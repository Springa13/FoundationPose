// main.h
#ifndef MAIN_H // include guard
#define MAIN_H

#include <raylib.h>
#include <math.h>
#include <cstdio>
#include <cstring>
#include "raymath.h"
#include <thread>
#include <chrono>
#include <iostream>
#include <fstream>
#include <vector>
#include <cfloat>


void LoadMaterialsFromMtl(Model *model, const char *mtlFile, const char *folderPath);
Matrix loadBin(int count);
BoundingBox TransformBoundingBox(BoundingBox bbox, Matrix transform);

#endif /* MY_CLASS_H */