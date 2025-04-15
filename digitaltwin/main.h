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

void LoadMaterialsFromMtl(Model *model, std::string mtlFile, std::string folderPath);
Matrix loadBin(int count);
bool newFrameDetected(int count);
BoundingBox TransformBoundingBox(BoundingBox bbox, Matrix transform);

#endif /* MAIN_H */