

/**
  * @brief : Check if a joint exist in the joint IDs array.

  * @param[in] int      jointID     The index of the joint to find.
  * @param[in] int[]    jointIDs    The list of joints.

  * @return int     The index of the joint ID in the joints array. Otherwise -1.
**/
int
jointExist(
    const   int     jointID;
    const   int     jointIDs[]
)
{
    for(int i=0; i<len(jointIDs); i++){
        if(jointIDs[i] == jointID){
            return i;
        }
    }

    return -1;
}

/**
  * @brief : Add a joint to the joints arrays.

  * @param[in] int      jointID         The index of the joint to add.
  * @param[io] int[]    jointIDs        The list of joint IDs.
  * @param[io] float[]  jointWeights    The list of joint weights.

  * @return int     The index of the joint ID in the joints array.
**/
int
addJoint(
    const   int     jointID;
    export  int     jointIDs[];
    export  float   jointWeights[]
)
{
    int jointLocalID = jointExist(jointID, jointIDs);

    if(jointLocalID == -1){
        jointLocalID = len(jointIDs);
        append(jointIDs, jointID);
        append(jointWeights, 0.0);
    }

    return jointLocalID;
}

/**
  * @brief : Remove a joint from the joint arrays.

  * @param[in]  int     jointID         The index of the joint to remove.
  * @param[io]  int[]   jointIDs        The list of the joint IDs.
  * @param[io]  float[] jointWeights    The list of the joint weihgts.
**/
void
removeJoint(
    const   int     jointID;
    export  int     jointIDs[];
    export  float   jointWeights[]
)
{
    jointLocalID = jointExist(jointID, jointIDs);
    
    if(jointLocalID > -1){
        removeindex(jointIDs, jointLocalID);
        removeindex(jointWeights, jointLocalID);
    }
}

float
setJointWeight(
    const   int     localJointID;
    const   float   jointWeight;
    const   int     setType;
    export  float   jointWeights[]
)
{
    // Get the current joint weight value.
    float jntWeight   = jointWeights[localJointID];

    // Check if the jointWeight is not greater than 1.0.
    if(jntWeight < 1.0){
        float jntAddValue = 0.0;
        // Compute the weight to add to the jointWeight.
        // Use the setType to define the way to compute the add value.
        if(setType == 0){           // Replace
            if(jntWeight < jointWeight){
                jntAddValue = jointWeight - jntWeight;
            }
        }else if(setType == 1){     // Add
            jntAddValue = jntWeight;
        }

        jntWeight += jntAddValue;

        // Clamp the joint weight value.
        if(jntWeight > 1.0){
            jntWeight = 1.0;
        }

        // Set the joint weight value.
        jointWeights[localJointID] = jntWeight;

        return jntWeight;
    }

    return 1.0;
}

void
normalizeSkinWeights(
    const int       skinJointIndex[];
    export float    skinJointWeights[]
)
{
    float cumulWeights = 0.0;

    for(int i=0; i<len(skinJointIndex); i++){
        cumulWeights += skinJointWeights[i];
    }

    if(cumulWeights > 0.0){
        for(int i=0; i<len(skinJointIndex); i++){
            skinJointWeights[i] /= cumulWeights;
        }
    }
}

void
normalizeOtherJointsWeight(
    const   int         localJointID;
    const   float       jointWeight;
    export  float       jointWeights[]
)
{
    if(jointWeight < 1.0){
        float otherMaxWeight    = 1.0 - jointWeight;

        float otherCumulWeight  = 0.0;

        for(int i=0; i<len(jointWeights); i++){
            if(i != localJointID){
                otherCumulWeight += jointWeights[i];
            }
        }

        if(otherCumulWeight > 0.0){
            for(int i=0; i<len(jointWeights); i++){
                if(i != localJointID){
                    jointWeights[i] = jointWeights[i] / otherCumulWeight;
                }
            }
        }
    }else{
        for(int i=0; i<len(jointWeights); i++){
            if(i != localJointID){
                jointWeights[i] = 0.0;
            }
        }
    }

}

void
pruneJointsWeights(
    const   float   minValue;
    export  int     jointIDs[];
    export  float   jointWeights[]
)
{
    int     newJointIDs[];
    float   newJointWeights[];

    for(int i=0; i<len(jointIDs); i++){
        if(jointWeights[i] >= minValue){
            append(newJointIDs, jointIDs[i]);
            append(newJointWeights, jointWeights[i]);
        }
    }

    jointIDs        = newJointIDs;
    jointWeights    = newJointWeights;
}

void
limitJointWeights(
    const   int     maxJointCount;
    export  int     jointIDs[];
    export  float   jointWeights[]
)
{
    if(len(jointIDs) > maxJointCount){
        int     newJointIDs[];
        float   newJointWeights[];

        int     ordering[]              = argsort(jointWeights);

        int     orderedJointIDs[]       = reverse(reorder(jointIDs, ordering));
        float   orderedJointWeights[]   = reverse(reorder(jointWeights, ordering));

        for(int i=0; i<maxJointCount; i++){
            append(newJointIDs, orderedJointIDs[i]);
            append(newJointWeights, orderedJointWeights[i]);
        }

        jointIDs        = newJointIDs;
        jointWeights    = newJointWeights;
    }
}


void
symmetryMap(
    const   int     pointID;
    const   vector  pointPos;
    const   int     symmetryAxis;
    const   float   tolerance;
    export  int     symID;
    export  int     symLocation
)
{
    symLocation = 0;
    // Store the point position in the symmetry Position.
    vector  symPos = pointPos;
    // Negate the position axis.
    if(symmetryAxis == 0){
        symPos.x *= -1.0;
        if(pointPos.x > 0.0){
            symLocation = 1;
        }else if(pointPos.x < 0.0){
            symLocation = -1;
        }
    }else if(symmetryAxis == 1){
        symPos.y *= -1.0;
        if(pointPos.y > 0.0){
            symLocation = 1;
        }else if(pointPos.y < 0.0){
            symLocation = -1;
        }
    }else if(symmetryAxis == 2){
        symPos.z *= -1.0;
        if(pointPos.z > 0.0){
            symLocation = 1;
        }else if(pointPos.z < 0.0){
            symLocation = -1;
        }
    }
    // Search the symmetry point.
    int     symPoints[] = pcfind(geoself(), "P", symPos, tolerance, 1);
    // If some symmetry points found. We use the first point. Otherwise use -1.
    symID       = -1;
    if(len(symPoints) > 0){
        symID = symPoints[0];
    }
}

void
symmetryMapColor(
    const   int         pointID;
    const   int         symID;
    const   int         symLocation;
    export  vector      pointColor
)
{
    vector positiveColor    = {0.9, 0.5, 0.0};
    vector negativeColor    = {0.0, 0.8, 0.8};
    vector centerColor      = {0.0, 0.9, 0.0};
    vector errorColor       = {5.0, 0.0, 0.0};

    pointColor              = errorColor;

    if(symID > -1){
        if(pointID == symID){
            pointColor = centerColor;
        }else{
            if(symLocation == 1){
                pointColor = positiveColor;
            }else if(symLocation == -1){
                pointColor = negativeColor;
            }
        }
    }

}





void
captureSkin(
    const int       jointGeoID;
    const int       computeNormal;
    const vector    pointPosition;
    const vector    pointNormal;
    const int       skinJointIndex[];
    const float     skinJointWeights[];
    export vector   skinJointPositions[];
    export vector   skinJointNormals[];

)
{

    resize(skinJointPositions, len(skinJointIndex));
    resize(skinJointNormals, len(skinJointIndex));

    // Loop over the joint.
    for(int i=0; i<len(skinJointIndex); i++){
        
        matrix3 jointRot    = point(jointGeoID, "transform", skinJointIndex[i]);
        matrix  jointTrans  = jointRot;
        vector  jointPos    = point(jointGeoID, "P", skinJointIndex[i]);
        jointTrans.ax       = jointPos.x;
        jointTrans.ay       = jointPos.y;
        jointTrans.az       = jointPos.z;

        skinJointPositions[i]  = pointPosition * invert(jointTrans);
        skinJointNormals[i]    = pointNormal * invert(jointRot);
    }
}

void
deformSkin(
    const int       jointGeoID;
    const int       jointComputeNormal;
    const int       skinJointIndex[];
    const float     skinJointWeights[];
    const vector    skinJointPositions[];
    const vector    skinJointNormals[];
    export vector   pointPosition;
    export vector   pointNormal
)
{

    // Define the average position and average normal.
    pointPosition   = {0.0, 0.0, 0.0};
    pointNormal     = {0.0, 0.0, 0.0};

    // Loop over the joints.
    for(int i=0; i<len(skinJointIndex); i++){

        matrix3 jointRot    = point(jointGeoID, "transform", skinJointIndex[i]);
        matrix  jointTrans  = jointRot;
        vector  jointPos    = point(jointGeoID, "P", skinJointIndex[i]);
        jointTrans.ax       = jointPos.x;
        jointTrans.ay       = jointPos.y;
        jointTrans.az       = jointPos.z;

        pointPosition       += skinJointPositions[i] * jointTrans * skinJointWeights[i];
        pointNormal         += skinJointNormals[i] * jointRot * skinJointWeights[i];
    }
}

void
skinColor(
    const int       colorStyle;
    const int       randomSeed;
    const int       colorSelectedJoint;
    const int       selectedJoint;
    const vector    selectedColor;
    const string    jointColorRamp;
    const int       skinJointIndex[];
    const float     skinJointWeights[];
    export vector   pointColor
)
{

    // Define the average color.
    pointColor = {0.0, 0.0, 0.0};

    if(colorStyle == 0){    // Randomly color all joints.
        // Loop over the skin joint.
        if(len(skinJointIndex) > 0){
            for(int i=0; i<len(skinJointIndex); i++){
                if(skinJointIndex[i] == selectedJoint){
                    if(colorSelectedJoint){
                        pointColor += selectedColor * skinJointWeights[i];
                    }else{
                        pointColor += vector(rand(skinJointIndex[i] + randomSeed)) * skinJointWeights[i];
                    }
                }else{
                    pointColor += vector(rand(skinJointIndex[i] + randomSeed)) * skinJointWeights[i];
                }
            }
        }
    }else if(colorStyle == 1){ // Color only the selected joint.
        float weight = 0.0;
        if(len(skinJointIndex) > 0){
            for(int i=0; i<len(skinJointIndex); i++){
                if(selectedJoint == skinJointIndex[i]){
                    weight = skinJointWeights[i];
                    break;
                }
            }
        }
        pointColor = chramp(jointColorRamp, weight);
    }else{ // No joint color.
        pointColor = {1.0, 1.0, 1.0};
    }
}

