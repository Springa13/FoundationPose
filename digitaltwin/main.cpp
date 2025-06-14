#include "main.h"

// float get_cam_K_fy() {



//     return fy;
// }

int main(int argc, char *argv[]) {
    
    // Initialize window and 3D camera
    SetConfigFlags(FLAG_VSYNC_HINT);
    InitWindow(1280, 720, "FoundationPose Digital Twin");

    std::string data_folder;
    bool simulation;
    float fy;
    int height;
    
    
    if (argc < 2) {
        data_folder = "mustard";
    } else { data_folder = argv[1]; }
    if (argc < 3) {
        simulation = true;
    } else { if (std::stoi(argv[2]) == 1) simulation = false; }
    if (argc < 4) {
        fy = 643.366f;
    } else { fy = std::stof(argv[3]); }
    if (argc < 5) {
        height = 720;
    } else { height = std::stoi(argv[4]); }
    

    std::stringstream folderPathTemplate;
    folderPathTemplate << "../output/" << data_folder << "/mesh";
    std::string folderPath = folderPathTemplate.str(); 

    std::stringstream posePathTemplate;
    posePathTemplate << "../output/" << data_folder << "/poses";
    std::string posePath = posePathTemplate.str(); 



    std::string objName = "box.obj";
    std::string mtlName = "box.mtl";

    // Load the OBJ model
    std::stringstream objPathTemplate;
    objPathTemplate << folderPath << "/" << objName;
    std::string objPath = objPathTemplate.str(); 
    
    Model model = LoadModel(objPath.c_str());
    

    // Load materials from .mtl file
    std::stringstream mtlPathTemplate;
    mtlPathTemplate << folderPath << "/" << mtlName;
    std::string mtlPath = mtlPathTemplate.str(); 

    LoadMaterialsFromMtl(&model, mtlPath, folderPath);

    // // Target size for all models
    BoundingBox bbox = GetModelBoundingBox(model);
    Vector3 center = {
        (bbox.min.x + bbox.max.x) / 2.0f,
        (bbox.min.y + bbox.max.y) / 2.0f,
        (bbox.min.z + bbox.max.z) / 2.0f
    };
    Matrix centerOffset = MatrixTranslate(-center.x, -center.y, -center.z);

    float scale = 10.0f;
    Matrix scaleMat = MatrixScale(scale, scale, scale);
    
    std::vector<double> times;
    
    if (simulation) {
        std::stringstream timingPathTemplate;
        timingPathTemplate << "../output/" << data_folder << "/timing.txt";
        std::string timingPath = timingPathTemplate.str(); 
        times = loadTimestampsFromFile(timingPath);
    }   

    Camera3D camera = { 0 };
    camera.position = (Vector3){ 0.0f, 0.0f, 0.1f };  // Move back slightly
    camera.target = (Vector3){ 0.0f, 0.0f, 0.0f };
    camera.up = (Vector3){ 0.0f, 1.0f, 0.0f };
    camera.fovy = 2 * atan(height / (2 * fy)) * RAD2DEG;  // Match fy
    

    //float rotationY = 0.0f; // Rotation around Y-axis (left/right)
    //float rotationX = 0.0f; // Rotation around X-axis (up/down)
    //float rotationZ = 0.0f;

    int frameNumber = 0;

    float scaleFactor = 0.0f;
    //float pos = 4.0f;

    using clock = std::chrono::steady_clock;
    auto last_run = clock::now();
    bool repeat = false;
    
    SetTargetFPS(60);

    while (!WindowShouldClose()) {
    	// Update camera position
    	UpdateCamera(&camera, CAMERA_CUSTOM);

        // Rotate camera left (A) or right (D)
        // Rotate left/right with arrow keys
        // if (IsKeyDown(KEY_RIGHT)) rotationY -= 0.5f;
        // if (IsKeyDown(KEY_LEFT)) rotationY += 0.5f;
        
        // // Rotate up/down with arrow keys
        // if (IsKeyDown(KEY_UP)) rotationX += 0.5f;
        // if (IsKeyDown(KEY_DOWN)) rotationX -= 0.5f;

        if (IsKeyDown(KEY_S)) scaleFactor = 0.01f;
        if (IsKeyDown(KEY_W)) scaleFactor = -0.01f;
        if (IsKeyDown(KEY_R)) repeat = true;

        if (repeat) {
            frameNumber = 0;
            repeat = false;
        }
        //pos += scaleFactor;
        //camera.position = (Vector3){ 0.0f, 0.0f, pos };  // Move back slightly
        // scale += scaleFactor;
        // scaleMat = MatrixScale(scale, scale, scale);
        // Offset and apply transformations
        Matrix pose = loadBin(frameNumber, posePath);

        // model.transform = MatrixMultiply(MatrixTranslate(modelOffset.x, modelOffset.y, modelOffset.z), mat); 
        Matrix rot = MatrixRotateZ(DEG2RAD * 180);

        model.transform = MatrixMultiply(centerOffset, MatrixMultiply(rot, pose));
           
        scaleFactor = 0;
        BeginDrawing();
        ClearBackground(BLACK);

        BeginMode3D(camera);
        
        DrawModel(model, Vector3Zero(), 1.0f, WHITE); // Draw model

        float axisLength = 100.0f;
        
        Vector3 xEnd = Vector3Transform({axisLength, 0, 0}, model.transform);
        Vector3 yEnd = Vector3Transform({0, axisLength, 0}, model.transform);
        Vector3 zEnd = Vector3Transform({0, 0, axisLength}, model.transform);
        Vector3 origin = Vector3Transform({0, 0, 0}, model.transform);;

        // Draw axes (length = 1.0 units)
        
        DrawLine3D(origin, xEnd, RED);   // X-axis
        DrawLine3D(origin, yEnd, GREEN); // Y-axis
        DrawLine3D(origin, zEnd, BLUE);  // Z-axis
        
        // DrawGrid(10, 1.0f);
        EndMode3D();

        std::stringstream frameTextTemplate;
        frameTextTemplate << "frame " << std::setw(6) << std::setfill('0') << frameNumber;
        std::string frameText = frameTextTemplate.str(); 
        DrawText(frameText.c_str(), 10, 10, 20, WHITE);
        DrawText("X", 10, 40, 20, RED);
        DrawText("Y", 40, 40, 20, GREEN);
        DrawText("Z", 70, 40, 20, BLUE);
        // DrawText(TextFormat("Current FPS: %i", GetFPS()), 10, 70, 20, GREEN);
        EndDrawing();

        if (newFrameDetected(frameNumber+1, posePath)) {
            
            if (simulation) {
                auto now = clock::now();
                std::chrono::duration<double> elapsed = now - last_run;
                //elapsed.count() >= times[frameNumber+1] || 
                
                if (elapsed.count() >= 0.09) {
                    frameNumber++;
                    printf("%f", elapsed.count());
                    last_run = now;
                }
                
            } else {
                frameNumber++;
            }
        }

        
     
    }

    // Cleanup resources
    // UnloadTexture(texture);
    UnloadModel(model);
    CloseWindow();
    return 0;
}

// Function to load textures from .mtl file and apply to model
void LoadMaterialsFromMtl(Model *model, std::string mtlFile, std::string folderPath)
{
    FILE *file = fopen(mtlFile.c_str(), "r");
    if (file == NULL)
    {
        printf("Failed to load .mtl file!\n");
        return;
    }

    char line[256];
    int currentMaterial = -1; // Index for materials

    while (fgets(line, sizeof(line), file))
    {
        if (strncmp(line, "newmtl", 6) == 0)  // New material definition
        {
            currentMaterial++;  // Increment material index
        }
        else if (strncmp(line, "map_Kd", 6) == 0) // Diffuse texture
        {
            char textureName[256];
            sscanf(line, "map_Kd %s", textureName);

            std::stringstream texturePathTemplate;
            texturePathTemplate << folderPath << "/" << textureName;
            std::string texturePath = texturePathTemplate.str();            
            
            // Check the texture path and load the texture
            Texture2D texture = LoadTexture(texturePath.c_str());  // Load diffuse texture
            if (currentMaterial >= 0 && currentMaterial < model->materialCount)
            {
                model->materials[currentMaterial].maps[MATERIAL_MAP_DIFFUSE].texture = texture;
            }
        }
        else if (strncmp(line, "map_Ks", 6) == 0) // Specular texture
        {
            char textureName[256];
            sscanf(line, "map_Ks %s", textureName);

            std::stringstream texturePathTemplate;
            texturePathTemplate << folderPath << "/" << textureName;
            std::string texturePath = texturePathTemplate.str(); 

            // Load specular texture
            Texture2D texture = LoadTexture(texturePath.c_str());  
            if (currentMaterial >= 0 && currentMaterial < model->materialCount)
            {
                model->materials[currentMaterial].maps[MATERIAL_MAP_SPECULAR].texture = texture;
            }
        }
    }

    fclose(file);
}

bool newFrameDetected(int count, std::string path) {
    
    std::stringstream ss;
    ss << path << "/frame" << std::setw(6) << std::setfill('0') << count << ".bin";
    std::string result = ss.str();
    bool detected;

    if (std::filesystem::exists(result)) {
        detected = true;
    } else {
        detected = false;
    }

    return detected;
}

Matrix loadBin(int count, std::string path)  {
    std::stringstream ss;
    ss << path << "/frame" << std::setw(6) << std::setfill('0') << count << ".bin";
    std::string result = ss.str();

    std::ifstream file(result, std::ios::binary);
    if (!file) {
        std::cerr << "File not found!\n";
        return MatrixIdentity();
    }

    std::vector<float> fpMatrix(16);  // 4x4 matrix (16 elements)
    file.read(reinterpret_cast<char*>(fpMatrix.data()), fpMatrix.size() * sizeof(float));

    // Convert to Raylib Matrix
    Matrix transform1 = {
        fpMatrix[0],  fpMatrix[1],  fpMatrix[2],  fpMatrix[3],
        -fpMatrix[4],  -fpMatrix[5],  -fpMatrix[6],  -fpMatrix[7],
        -fpMatrix[8],  -fpMatrix[9],  -fpMatrix[10], -fpMatrix[11],
        fpMatrix[12],  fpMatrix[13], fpMatrix[14], fpMatrix[15]
    };

    return transform1;
}

std::vector<double> loadTimestampsFromFile(const std::string& filename) {
    std::vector<double> timestamps;
    std::ifstream file(filename);
    std::string line;

    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        return timestamps;
    }

    while (std::getline(file, line)) {
        try {
            double value = std::stod(line);
            timestamps.push_back(value);
        } catch (const std::invalid_argument& e) {
            std::cerr << "Invalid number in line: " << line << std::endl;
        }
    }

    file.close();
    return timestamps;
}
