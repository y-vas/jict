#define NPY_NO_DEPRECATED_API	NPY_1_8_API_VERSION
#define PY_ARRAY_UNIQUE_SYMBOL	SHARED_ARRAY_ARRAY_API
#define NO_IMPORT_ARRAY

#include <Python.h>
#include <numpy/arrayobject.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include "shared_array.h"
#include "map_owner.h"

static PyObject *do_create(const char *name, int ndims, npy_intp *dims ) {
	struct array_meta *meta;
	size_t size;
	size_t map_size;
	void *map_addr;
	int i;
	int fd;
	struct stat file_info;
	PyObject *array;
	PyMapOwnerObject *map_owner;
	PyArray_Descr *dtype = NULL;

	dtype = PyArray_DescrFromType(NPY_DEFAULT_TYPE);

	/* Calculate the memory size of the array */
	size = dtype->elsize;
	for (i = 0; i < ndims; i++){
		size *= dims[i];
	}

	/* Calculate the size of the mmap'd area */
	map_size = size + sizeof (*meta);
	printf("%s", map_size );

	/* Create the file */
	if ((fd = open_file( name, O_RDWR | O_CREAT | O_EXCL, 0666)) < 0){
		return PyErr_SetFromErrnoWithFilename(PyExc_OSError, name);
		// unlink_file(name);
		//
		// if ((fd = open_file( name, O_RDWR | O_CREAT | O_EXCL, 0666)) < 0)
		// 	return PyErr_SetFromErrnoWithFilename(PyExc_OSError, name);
	}

	/* Grow the file */
	if (ftruncate(fd, map_size) < 0) {
		close(fd);
		return PyErr_SetFromErrnoWithFilename(PyExc_OSError, name);
	}

	/* Find the actual file size after growing (on some systems it rounds
	 * up to 4K) */
	if (fstat(fd, &file_info) < 0) {
		close(fd);
		return PyErr_SetFromErrnoWithFilename(PyExc_OSError, name);
	}
	map_size = file_info.st_size;

	/* Map it */
	map_addr = mmap(NULL, map_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
	close(fd);
	if (map_addr == MAP_FAILED)
		return PyErr_SetFromErrnoWithFilename(PyExc_OSError, name);

	/* Append the meta-data to the array in memory */
	meta = (struct array_meta *) (map_addr + (map_size - sizeof (*meta)));
	strncpy(meta->magic, SHARED_ARRAY_MAGIC, sizeof (meta->magic));
	meta->size     = size;
	meta->typenum  = dtype->type_num;
	meta->itemsize = dtype->elsize;
	meta->ndims    = ndims;
	for (i = 0; i < ndims; i++)
		meta->dims[i] = dims[i];

	/* Hand over the memory map to a MapOwner instance */
	map_owner = PyObject_MALLOC(sizeof (*map_owner));
	PyObject_INIT((PyObject *) map_owner, &PyMapOwner_Type);
	map_owner->map_addr = map_addr;
	map_owner->map_size = map_size;
	map_owner->name = strdup(name);

	/* Create the array object */
	array = PyArray_New(&PyArray_Type, meta->ndims, meta->dims,
	                    meta->typenum, NULL, map_addr, meta->itemsize,
	                    NPY_ARRAY_CARRAY, NULL);

	/* Attach MapOwner to the array */
	PyArray_SetBaseObject((PyArrayObject *) array, (PyObject *) map_owner);
	return array;
}

/*
 * Method: SharedArray.create()
 */
PyObject *shared_array_create( PyObject *self, PyObject *args, PyObject *kwds ){
	static char *kwlist[] = { "name", "shape" , NULL };
	const char *name;
	PyArray_Dims shape = { NULL, 0 };
	PyObject *ret = NULL;

	/* Parse the arguments */
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "sO&|O&", kwlist,
					 &name, PyArray_IntpConverter, &shape ))
		goto out;

	ret = do_create( name , 1 , shape.ptr );

out:	/* Clean-up on exit */
	if (shape.ptr)
		PyDimMem_FREE(shape.ptr);

	return ret;
}
