

cdef class _SpatialHash:
    cdef int cell_size
    cdef dict contents
    cdef dict buckets_for_sprites

    def __cinit__(self, int cell_size):
        self.cell_size = cell_size
        self.contents = {}
        self.buckets_for_sprites = {}

    cpdef _hash(self, int x, int y):
        return x // self.cell_size, y // self.cell_size

    def reset(self):
        self.contents = {}

    def insert_object_for_box(self, object new_object):
        cdef int min_x = new_object.left
        cdef int max_x = new_object.right
        cdef int min_y = new_object.bottom
        cdef int max_y = new_object.top

        min_point = self._hash(min_x, min_y)
        max_point = self._hash(max_x, max_y)
