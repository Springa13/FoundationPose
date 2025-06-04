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
#include <sstream>
#include <iomanip>
#include <filesystem>

void LoadMaterialsFromMtl(Model *model, std::string mtlFile, std::string folderPath);
Matrix loadBin(int count, std::string path);
bool newFrameDetected(int , std::string path);
std::vector<double> loadTimestampsFromFile(const std::string& filename);

#endif /* MAIN_H */