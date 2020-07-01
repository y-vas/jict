#include <sys/types.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include "shared_array.h"

#define PREFIX_SHM	"shm://"

int open_file(const char *name, int flags, mode_t mode) {
	/* POSIX SHM */
	if (!strncmp(name, PREFIX_SHM, strlen(PREFIX_SHM)))
		return shm_open(name + strlen(PREFIX_SHM), flags, mode);

	/* For backward compatibility, assume POSIX SHM by default */
	if (!strstr(name, "://"))
		return shm_open(name, flags, mode);

	errno = EINVAL;
	return -1;
}

int unlink_file(const char *name) {
	/* POSIX SHM */
	if (!strncmp(name, PREFIX_SHM, strlen(PREFIX_SHM)))
		return shm_unlink(name + strlen(PREFIX_SHM));

	/* For backward compatibility, assume POSIX SHM by default */
	if (!strstr(name, "://"))
		return shm_unlink(name);

	errno = EINVAL;
	return -1;
}
