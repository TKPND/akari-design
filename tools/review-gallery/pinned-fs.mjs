import { closeSync, constants, openSync, realpathSync } from "node:fs";
import {
  mkdir,
  open,
  readdir,
  rename,
  rm,
} from "node:fs/promises";
import {
  isAbsolute,
  relative,
} from "node:path";

const directoryFlags =
  constants.O_RDONLY | constants.O_DIRECTORY | constants.O_NOFOLLOW;

function invalidPath() {
  const error = new Error("path escapes pinned dataRoot");
  error.code = "EACCES";
  return error;
}

function validateName(name) {
  if (
    typeof name !== "string" ||
    name.length === 0 ||
    name === "." ||
    name === ".." ||
    name.includes("/") ||
    name.includes("\\") ||
    name.includes("\0")
  ) {
    throw invalidPath();
  }
  return name;
}

function descriptorPath(fd, name) {
  return `/proc/${process.pid}/fd/${fd}/${validateName(name)}`;
}

export function createPinnedRoot(dataRoot) {
  const canonicalRoot = realpathSync(dataRoot);
  let rootFd = openSync("/", directoryFlags);
  try {
    for (const part of canonicalRoot.split("/").filter(Boolean)) {
      const nextFd = openSync(descriptorPath(rootFd, part), directoryFlags);
      closeSync(rootFd);
      rootFd = nextFd;
    }
  } catch (error) {
    closeSync(rootFd);
    throw error;
  }
  let activeLeases = 0;
  let closeRequested = false;
  let closed = false;

  function closeIfIdle() {
    if (!closeRequested || activeLeases !== 0 || closed) return;
    closed = true;
    closeSync(rootFd);
  }

  async function withLease(work) {
    if (closed) throw new Error("pinned dataRoot is closed");
    activeLeases += 1;
    try {
      return await work();
    } finally {
      activeLeases -= 1;
      closeIfIdle();
    }
  }

  function partsFor(path) {
    if (typeof path !== "string") throw invalidPath();
    const pathFromRoot = isAbsolute(path)
      ? relative(canonicalRoot, path)
      : path;
    if (
      isAbsolute(pathFromRoot) ||
      pathFromRoot === ".." ||
      pathFromRoot.startsWith("../") ||
      pathFromRoot.startsWith("..\\")
    ) {
      throw invalidPath();
    }
    if (pathFromRoot === "") return [];
    return pathFromRoot.split(/[\\/]/).map(validateName);
  }

  async function openDirectory(parts) {
    if (closed) throw new Error("pinned dataRoot is closed");
    let ownedHandle;
    let currentFd = rootFd;
    try {
      for (const part of parts) {
        const nextHandle = await open(
          descriptorPath(currentFd, part),
          directoryFlags,
        );
        await ownedHandle?.close();
        ownedHandle = nextHandle;
        currentFd = nextHandle.fd;
      }
      return ownedHandle;
    } catch (error) {
      await ownedHandle?.close();
      throw error;
    }
  }

  async function withDirectory(path, work) {
    return withLease(async () => {
      const handle = await openDirectory(partsFor(path));
      try {
        return await work(handle?.fd ?? rootFd);
      } finally {
        await handle?.close();
      }
    });
  }

  async function readAt(fd, name, encoding) {
    const handle = await open(
      descriptorPath(fd, name),
      constants.O_RDONLY | constants.O_NOFOLLOW,
    );
    try {
      return await handle.readFile(encoding);
    } finally {
      await handle.close();
    }
  }

  async function writeAt(fd, name, data, encoding) {
    const handle = await open(
      descriptorPath(fd, name),
      constants.O_WRONLY |
        constants.O_CREAT |
        constants.O_TRUNC |
        constants.O_NOFOLLOW,
      0o600,
    );
    try {
      await handle.writeFile(data, encoding);
    } finally {
      await handle.close();
    }
  }

  function directoryContext(fd) {
    return {
      fd,
      path(name) {
        return descriptorPath(fd, name);
      },
      readFile(name, encoding) {
        return readAt(fd, name, encoding);
      },
      writeFile(name, data, encoding) {
        return writeAt(fd, name, data, encoding);
      },
      mkdir(name, options) {
        return mkdir(descriptorPath(fd, name), options);
      },
      readdir(name, options) {
        return readdir(descriptorPath(fd, name), options);
      },
      remove(name, options) {
        return rm(descriptorPath(fd, name), options);
      },
      openDirectory(name) {
        return open(descriptorPath(fd, name), directoryFlags);
      },
      async withDirectory(name, work) {
        const handle = await open(descriptorPath(fd, name), directoryFlags);
        try {
          return await work(directoryContext(handle.fd));
        } finally {
          await handle.close();
        }
      },
      renameTo(sourceName, destination, destinationName) {
        return rename(
          descriptorPath(fd, sourceName),
          descriptorPath(destination.fd, destinationName),
        );
      },
    };
  }

  async function withParent(path, work) {
    return withLease(async () => {
      const parts = partsFor(path);
      if (parts.length === 0) throw invalidPath();
      const name = parts.pop();
      const handle = await openDirectory(parts);
      try {
        return await work(directoryContext(handle?.fd ?? rootFd), name);
      } finally {
        await handle?.close();
      }
    });
  }

  async function ensureDirectory(path) {
    return withLease(async () => {
      const parts = partsFor(path);
      let ownedHandle;
      let currentFd = rootFd;
      try {
        for (const part of parts) {
          const childPath = descriptorPath(currentFd, part);
          let nextHandle;
          try {
            nextHandle = await open(childPath, directoryFlags);
          } catch (error) {
            if (error.code !== "ENOENT") throw error;
            await mkdir(childPath);
            nextHandle = await open(childPath, directoryFlags);
          }
          await ownedHandle?.close();
          ownedHandle = nextHandle;
          currentFd = nextHandle.fd;
        }
      } finally {
        await ownedHandle?.close();
      }
    });
  }

  const fileSystem = {
    readFile(path, encoding) {
      return withParent(path, (parent, name) =>
        parent.readFile(name, encoding)
      );
    },
    writeFile(path, data, encoding) {
      return withParent(path, (parent, name) =>
        parent.writeFile(name, data, encoding)
      );
    },
    async copyFile(source, destination) {
      const contents = await fileSystem.readFile(source);
      await fileSystem.writeFile(destination, contents);
    },
    mkdir(path) {
      return ensureDirectory(path);
    },
    rename(source, destination) {
      return withParent(source, (sourceParent, sourceName) =>
        withParent(destination, (destinationParent, destinationName) =>
          sourceParent.renameTo(
            sourceName,
            destinationParent,
            destinationName,
          )
        )
      );
    },
  };

  return {
    canonicalRoot,
    fileSystem,
    withLease,
    withParent,
    readdir(path, options) {
      return withDirectory(path, (fd) =>
        readdir(`/proc/${process.pid}/fd/${fd}`, options)
      );
    },
    close() {
      closeRequested = true;
      closeIfIdle();
    },
  };
}
