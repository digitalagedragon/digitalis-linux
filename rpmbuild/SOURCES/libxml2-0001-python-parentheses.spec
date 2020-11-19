--- a/python/libxml.c
+++ b/python/libxml.c
@@ -294,7 +294,7 @@ xmlPythonFileReadRaw (void * context, char * buffer, int len) {
 	lenread = PyBytes_Size(ret);
 	data = PyBytes_AsString(ret);
 #ifdef PyUnicode_Check
-    } else if PyUnicode_Check (ret) {
+    } else if (PyUnicode_Check (ret)) {
 #if PY_VERSION_HEX >= 0x03030000
         Py_ssize_t size;
 	const char *tmp;
@@ -359,7 +359,7 @@ xmlPythonFileRead (void * context, char * buffer, int len) {
 	lenread = PyBytes_Size(ret);
 	data = PyBytes_AsString(ret);
 #ifdef PyUnicode_Check
-    } else if PyUnicode_Check (ret) {
+    } else if (PyUnicode_Check (ret)) {
 #if PY_VERSION_HEX >= 0x03030000
         Py_ssize_t size;
 	const char *tmp;
--- a/python/types.c
+++ b/python/types.c
@@ -602,16 +602,16 @@ libxml_xmlXPathObjectPtrConvert(PyObject *obj)
     if (obj == NULL) {
         return (NULL);
     }
-    if PyFloat_Check (obj) {
+    if (PyFloat_Check (obj)) {
         ret = xmlXPathNewFloat((double) PyFloat_AS_DOUBLE(obj));
-    } else if PyLong_Check(obj) {
+    } else if (PyLong_Check(obj)) {
 #ifdef PyLong_AS_LONG
         ret = xmlXPathNewFloat((double) PyLong_AS_LONG(obj));
 #else
         ret = xmlXPathNewFloat((double) PyInt_AS_LONG(obj));
 #endif
 #ifdef PyBool_Check
-    } else if PyBool_Check (obj) {
+    } else if (PyBool_Check (obj)) {
 
         if (obj == Py_True) {
           ret = xmlXPathNewBoolean(1);
@@ -620,14 +620,14 @@ libxml_xmlXPathObjectPtrConvert(PyObject *obj)
           ret = xmlXPathNewBoolean(0);
         }
 #endif
-    } else if PyBytes_Check (obj) {
+    } else if (PyBytes_Check (obj)) {
         xmlChar *str;
 
         str = xmlStrndup((const xmlChar *) PyBytes_AS_STRING(obj),
                          PyBytes_GET_SIZE(obj));
         ret = xmlXPathWrapString(str);
 #ifdef PyUnicode_Check
-    } else if PyUnicode_Check (obj) {
+    } else if (PyUnicode_Check (obj)) {
 #if PY_VERSION_HEX >= 0x03030000
         xmlChar *str;
 	const char *tmp;
@@ -650,7 +650,7 @@ libxml_xmlXPathObjectPtrConvert(PyObject *obj)
 	ret = xmlXPathWrapString(str);
 #endif
 #endif
-    } else if PyList_Check (obj) {
+    } else if (PyList_Check (obj)) {
         int i;
         PyObject *node;
         xmlNodePtr cur;
