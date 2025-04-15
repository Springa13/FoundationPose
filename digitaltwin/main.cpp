#include "main.h"
#include <sstream>
#include <iomanip>
#include <filesystem>

Vector3 MatrixToEuler(Matrix mat) {
    Vector3 euler;

    // Extract the 3x3 rotation portion of the 4x4 matrix
    float m00 = mat.m0, m01 = mat.m1, m02 = mat.m2;
    float m10 = mat.m4, m11 = mat.m5, m12 = mat.m6;
    float m20 = mat.m8, m21 = mat.m9, m22 = mat.m10;
    // std::cout << "m0 = " << m00 << ", m1 = " << m01 << ", m2 = " << m02 << ", m3 = " << mat.m3 << std::endl;
    // std::cout << "m4 = " << m10 << ", m5 = " << m11 << ", m6 = " << m12 << ", m7 = " << mat.m7 << std::endl;
    // std::cout << "m8 = " << m20 << ", m9 = " << m21 << ", m10 = " << m22 << ", m11 = " << mat.m11 <<  std::endl;
    // std::cout << "m12 = " << mat.m12 << ", m13 = " << mat.m13 << ", m14 = " << mat.m14 << ", m15 = " << mat.m15 <<  std::endl;

    // Yaw (rotation around Y-axis)
    euler.x = atan2f(m21, m22);

    // Pitch (rotation around X-axis)
    euler.y = atan2f(-m20, sqrtf(m21 * m21 + m22 * m22));

    // Roll (rotation around Z-axis)
    euler.z = atan2f(m10, m00);

    return euler;
}


int main(int argc, char *argv[]) {
    
    // Initialize window and 3D camera
    InitWindow(800, 600, "Raylib OBJ Model Loader");

    char *data_folder = argv[1];

    std::stringstream folderPathTemplate;
    folderPathTemplate << "../data/" << data_folder << "/mesh";
    std::string folderPath = folderPathTemplate.str(); 

    std::string objName = "textured_simple.obj";
    std::string mtlName = "textured_simple.mtl";

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

    // Get the bounding box
    BoundingBox box = GetModelBoundingBox(model);

    // Calculate model dimensions
    float modelWidth = box.max.x - box.min.x;
    float modelHeight = box.max.y - box.min.y;
    float modelDepth = box.max.z - box.min.z;

    // Find the largest dimension
    float maxDimension = fmaxf(fmaxf(modelWidth, modelHeight), modelDepth);

    // Target size for all models
    // float targetSize = 1.0f;
    // float scaleFactor = targetSize + (0.001*maxDimension/0.2);
    float scaleFactor = 1.8;

    // Calculate model center and offset it to (0,0,0)
    Vector3 modelCenter = {
        (box.min.x + box.max.x) / 2.0f,
        (box.min.y + box.max.y) / 2.0f,
        (box.min.z + box.max.z) / 2.0f
    };
    Vector3 modelOffset = { -modelCenter.x, -modelCenter.y, -modelCenter.z };

    // Camera setup
    Camera camera = { 0 };
    camera.target = (Vector3){ 0.0f, 0.0f, 0.0f }; // Always look at model center
    camera.position = (Vector3){ 0.0f, maxDimension * 2.0f, maxDimension * 3.0f };
    camera.up = (Vector3){ 0.0f, 1.0f, 0.0f };
    camera.fovy = 45.0f;
    camera.projection = CAMERA_PERSPECTIVE;

    float rotationY = 0.0f; // Rotation around Y-axis (left/right)
    float rotationX = 0.0f; // Rotation around X-axis (up/down)
    float rotationZ = 0.0f;

    int frameNumber = 0;

    SetTargetFPS(60);

    while (!WindowShouldClose()) {
    	// Update camera position
    	UpdateCamera(&camera, CAMERA_CUSTOM);

        // Rotate camera left (A) or right (D)
        // Rotate left/right with arrow keys
        if (IsKeyDown(KEY_RIGHT)) rotationY -= 0.5f;
        if (IsKeyDown(KEY_LEFT)) rotationY += 0.5f;
        

        // Rotate up/down with arrow keys
        if (IsKeyDown(KEY_UP)) rotationX += 0.5f;
        if (IsKeyDown(KEY_DOWN)) rotationX -= 0.5f;


        if (IsKeyDown(KEY_S)) scaleFactor -= 0.1f;
        if (IsKeyDown(KEY_W)) scaleFactor += 0.1f;

        if (IsKeyDown(KEY_A)) rotationZ += 0.5f;
        if (IsKeyDown(KEY_D)) rotationZ -= 0.5f;

        // Apply rotation in both X and Y directions
        Matrix rotationYMatrix = MatrixRotateY(DEG2RAD * rotationY);
        Matrix rotationXMatrix = MatrixRotateX(DEG2RAD * rotationX);
        Matrix rotationZMatrix = MatrixRotateZ(DEG2RAD * rotationZ);
        
        // Offset and apply transformations
        Matrix mat = loadBin(frameNumber);
        Vector3 euler = MatrixToEuler(mat);
        std::cout << "Euler angles: X = " << (RAD2DEG * euler.x) << ", Y = " << (RAD2DEG * euler.y) << ", Z = " << (RAD2DEG * euler.z) << std::endl;
        
        Matrix newmat = MatrixIdentity();
        Matrix xrot = MatrixRotateX(-PI);  // Convert Y-up to Z-up
        //newmat = MatrixMultiply(xrot, newmat);
        Matrix zrot = MatrixRotateZ(PI / 8);  // Convert Y-up to Z-up
        //newmat = MatrixMultiply(zrot, newmat);

        Matrix rotate = MatrixRotateXYZ(euler);
        newmat = MatrixMultiply(newmat, rotate);
        model.transform = MatrixMultiply(MatrixTranslate(modelOffset.x, modelOffset.y, modelOffset.z), newmat);        
        BoundingBox bbox = GetModelBoundingBox(model); // Get bounding box
        bbox = TransformBoundingBox(bbox, model.transform);  // Apply transformations

        BeginDrawing();
        ClearBackground(RAYWHITE);

        BeginMode3D(camera);
        DrawModel(model, modelOffset, scaleFactor, WHITE); // Draw model
        DrawBoundingBox(bbox, RED);

        Vector3 modelPos = { model.transform.m12, model.transform.m13, model.transform.m14 }; // Model position

        Vector3 right = Vector3Transform({ 1, 0, 0 }, model.transform); // Local X-axis
        Vector3 up    = Vector3Transform({ 0, 1, 0 }, model.transform); // Local Y-axis
        Vector3 forward = Vector3Transform({ 0, 0, 1 }, model.transform); // Local Z-axis

        DrawLine3D(modelPos, right, RED);   // Model X-axis
        DrawLine3D(modelPos, up, GREEN);    // Model Y-axis
        DrawLine3D(modelPos, forward, BLUE);// Model Z-axis
        // DrawGrid(10, 1.0f);
        EndMode3D();

        if (newFrameDetected(frameNumber+1)) {
            frameNumber++;
        }
        
        DrawText("Use mouse to orbit camera", 10, 10, 20, DARKGRAY);
        EndDrawing();
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

bool newFrameDetected(int count) {
    std::stringstream ss;
    ss << "../output/poses/frame" << std::setw(6) << std::setfill('0') << count << ".bin";
    std::string result = ss.str();

    bool detected;

    if (std::filesystem::exists(result)) {
        detected = true;
    } else {
        detected = false;
    }

    return detected;
}

Matrix loadBin(int count)  {
    std::stringstream ss;
    ss << "../output/poses/frame" << std::setw(6) << std::setfill('0') << count << ".bin";
    std::string result = ss.str();

    std::ifstream file(result, std::ios::binary);
    if (!file) {
        std::cerr << "File not found!\n";
        return MatrixIdentity();
    }

    std::vector<float> array(16);  // 4x4 matrix (16 elements)
    file.read(reinterpret_cast<char*>(array.data()), array.size() * sizeof(float));

    // Convert to Raylib Matrix
    Matrix transform = {
        array[0],  array[1],  array[2],  0,
        array[4],  array[5],  array[6],  0,
        array[8],  array[9],  array[10], 0,
        array[12], array[13], array[14], 1
    };

    return transform;
}

BoundingBox TransformBoundingBox(BoundingBox bbox, Matrix transform) {
    Vector3 corners[8] = {
        bbox.min, bbox.max,
        { bbox.min.x, bbox.min.y, bbox.max.z },
        { bbox.min.x, bbox.max.y, bbox.min.z },
        { bbox.max.x, bbox.min.y, bbox.min.z },
        { bbox.min.x, bbox.max.y, bbox.max.z },
        { bbox.max.x, bbox.min.y, bbox.max.z },
        { bbox.max.x, bbox.max.y, bbox.min.z }
    };

    Vector3 newMin = { FLT_MAX, FLT_MAX, FLT_MAX };
    Vector3 newMax = { -FLT_MAX, -FLT_MAX, -FLT_MAX };

    for (int i = 0; i < 8; i++) {
        corners[i] = Vector3Transform(corners[i], transform);
        newMin = Vector3Min(newMin, corners[i]);
        newMax = Vector3Max(newMax, corners[i]);
    }

    return { newMin, newMax };
}
