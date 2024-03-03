#ifndef __FRANKENSTEIN_JOINT_ORIENT__
#define __FRANKENSTEIN_JOINT_ORIENT__

#include <frankenstein_skeletonConstants.h>

void 
matrixToVector(
    const matrix3   mat;
    export vector   axisX;
    export vector   axisY;
    export vector   axisZ
)
{
    axisX   = normalize(vector(set(mat.xx, mat.xy, mat.xz)));
    axisY   = normalize(vector(set(mat.yx, mat.yy, mat.yz)));
    axisZ   = normalize(vector(set(mat.zx, mat.zy, mat.zz)));
}

void
vectorToMatrix(
    const vector    axisX;
    const vector    axisY;
    const vector    axisZ;
    export matrix3  mat
)
{
    mat = set(
        axisX.x, axisX.y, axisX.z,
        axisY.x, axisY.y, axisY.z,
        axisZ.x, axisZ.y, axisZ.z
    );
}

vector
getAxis(
    const int       axis;
    const matrix3   transform
)
{
    vector mainAxis;
    if(axis == 0){
        mainAxis = set(transform.xx, transform.xy, transform.xz);
    }else if(axis == 1){
        mainAxis = set(transform.yx, transform.yy, transform.yz);
    }else if(axis == 2){
        mainAxis = set(transform.zx, transform.zy, transform.zz);
    }else if(axis == 3){
        mainAxis = set(-transform.xx, -transform.xy, -transform.xz);
    }else if(axis == 4){
        mainAxis = set(-transform.yx, -transform.yy, -transform.yz);
    }else if(axis == 5){
        mainAxis = set(-transform.zx, -transform.zy, -transform.zz);
    }

    return normalize(mainAxis);
}

void
filterAxis(
    const vector    axis;
    const int       target;
    export vector   axisX;
    export vector   axisY;
    export vector   axisZ
)
{
    if(target == 0 || target == 3){
        axisX = axis;
    }else if(target == 1 || target == 4){
        axisY = axis;
    }else if(target == 2 || target == 5){
        axisZ = axis;
    }
}

matrix3
buildTransformFromAxis(
    const vector    axis0;
    const vector    axis1;
    const int       axis0Target;
    const int       axis1Target
)
{
    vector axisX, axisY, axisZ;

     setpointattrib(GEO_SKELETON, "inBuildTransform", 1, "YOUHOU");

    // Filter axis 0.
    if(axis0Target >= 0 && axis0Target <= 2){
        filterAxis(axis0, axis0Target, axisX, axisY, axisZ);
    }
    else if(axis0Target >= 3 && axis0Target <= 5){
        filterAxis(-axis0, axis0Target, axisX, axisY, axisZ);
    }

    // Filter axis 1.
    if(axis1Target >= 0 && axis1Target <= 2){
        filterAxis(axis1, axis1Target, axisX, axisY, axisZ);
    }
    else if(axis1Target >= 3 && axis1Target <= 5){
        filterAxis(-axis1, axis1Target, axisX, axisY, axisZ);
    }

    // Make axis orthogonal.
    if(axis0Target == 0 || axis0Target == 3){
        if(axis1Target == 1 || axis1Target == 4){
            setpointattrib(GEO_SKELETON, "axisScenario", 1, "XY");
            axisZ = normalize(cross(axisX, axisY));
            axisY = normalize(cross(axisZ, axisX));
        }else if(axis1Target == 2 || axis1Target == 5){
            setpointattrib(GEO_SKELETON, "axisScenario", 1, "XZ");
            axisY = normalize(cross(axisZ, axisX));
            axisZ = normalize(cross(axisX, axisY));
        }
    }else if(axis0Target == 1 || axis0Target == 4){
        if(axis1Target == 0 || axis1Target == 3){
            setpointattrib(GEO_SKELETON, "axisScenario", 1, "YX");
            axisZ = normalize(cross(axisX, axisY));
            axisX = normalize(cross(axisY, axisZ));
        }else if(axis1Target == 2 || axis1Target == 5){
            setpointattrib(GEO_SKELETON, "axisScenario", 1, "YZ");
            axisX = normalize(cross(axisY, axisZ));
            axisZ = normalize(cross(axisX, axisY));
        }
    }else if(axis0Target == 2 || axis0Target == 5){
        if(axis1Target == 0 || axis1Target == 3){
            setpointattrib(GEO_SKELETON, "axisScenario", 1, "ZX");
            axisY = normalize(cross(axisZ, axisX));
            axisX = normalize(cross(axisY, axisZ));
        }else if(axis1Target == 1 || axis1Target == 4){
            setpointattrib(GEO_SKELETON, "axisScenario", 1, "ZY");
            axisX = normalize(cross(axisY, axisZ));
            axisY = normalize(cross(axisZ, axisX));
        }
    }

    // Return and build the matrix.
    return set(
        axisX.x, axisX.y, axisX.z,
        axisY.x, axisY.y, axisY.z,
        axisZ.x, axisZ.y, axisZ.z
    );
}

void
jointOrient(
    const vector    jointPos;
    const vector    targetDirPosition;
    const int       targetDirAxis;
    const int       useOrientRules;
    const int       mainAxis;
    const int       secondaryAxis;
    const int       lockedAxis;
    export matrix3  jointTransform

)
{
    setdetailattrib(GEO_SKELETON, "tempOrient", "Joint Orient");

    vector toTarget = normalize(targetDirPosition - jointPos);

    if(useOrientRules == 0){

        if(lockedAxis == -1){
            vector  refAxis      = getAxis(targetDirAxis, jointTransform);
            matrix3 rotation     = dihedral(refAxis, toTarget);
            jointTransform      *= rotation;
            setdetailattrib(GEO_SKELETON, "temp", "Orient No Rules No Lock");
        }else{
            vector axis0 = getAxis(lockedAxis, jointTransform);
            vector axis1 = toTarget;
            jointTransform = buildTransformFromAxis(axis0, axis1, lockedAxis, targetDirAxis);
            setpointattrib(GEO_SKELETON, "temp", 1, "Orient No Rules Locked");
            setpointattrib(GEO_SKELETON, "axis0", 1, axis0);
            setpointattrib(GEO_SKELETON, "axis1", 1, axis1);
            setpointattrib(GEO_SKELETON, "axis0Target", 1, lockedAxis);
            setpointattrib(GEO_SKELETON, "axis1Target", 1, targetDirAxis);

        }
    }else{

        vector axis0 = toTarget;
        vector axis1 = getAxis(secondaryAxis, jointTransform);
        jointTransform = buildTransformFromAxis(axis0, axis1, mainAxis, secondaryAxis);
        setdetailattrib(GEO_SKELETON, "temp", "Orient Ruled");

    }
}


void
alignAxis(
    const int       geoID;
    const int       jointID;
    const int       skinGeoID;
    const int       axisToAlign;
    const int       axisToLock;
    const int       targetJointID;
    const int       targetSkinPointID;
    const int       snapToJoint;
    const int       snapToSkin;
    const int       snapToJointAxis;
    const int       targetJointAxis;
    const vector    rayOrigin;
    const vector    rayDirection
)
{
    // Get the current joint transform matrix and extract the axis.
    vector  axisX, axisY, axisZ;
    matrix3 jointTransform = point(geoID, "transform", jointID);
    matrixToVector(jointTransform, axisX, axisY, axisZ);

    // Store the main axis from the user axis selection.
    vector mainAxis = axisX;
    if(axisToAlign == 1){
        mainAxis = axisY;
    }else if(axisToAlign == 2){
        mainAxis = axisZ;
    }else if(axisToAlign == 3){
        mainAxis = -axisX;
    }else if(axisToAlign == 4){
        mainAxis = -axisY;
    }else if(axisToAlign == 5){
        mainAxis = -axisZ;
    }

    // Store the locked axis from the user choice.
    vector lockedAxis = axisX;
    if(axisToLock == 2){
        lockedAxis = axisY;
    }else if(axisToLock == 3){
        lockedAxis = axisZ;
    }

    // Compute the direction of the axis that its used to align the main axis.
    vector jointPos = point(geoID, "P", jointID);
    vector targetPos;
    vector jointDist    = length(jointPos - rayOrigin);
    targetPos           = rayDirection * jointDist + rayOrigin;

    if(snapToJoint == 1 && targetJointID > -1){
        targetPos = point(geoID, "P", targetJointID);
    }

    if(snapToSkin == 1 && targetSkinPointID > -1){
        targetPos = point(skinGeoID, "P", targetSkinPointID);
    }

    vector dirAxis = normalize(targetPos - jointPos);

    if(snapToJointAxis == 1 && targetJointID > -1 && targetJointAxis > -1){
        matrix3 targetJointTransform = point(geoID, "transform", targetJointID);
        vector targetAxisX, targetAxisY, targetAxisZ;
        matrixToVector(targetJointTransform, targetAxisX, targetAxisY, targetAxisZ);

        if(targetJointAxis == 0){
            dirAxis = targetAxisX;
        }else if(targetJointAxis == 1){
            dirAxis = targetAxisY;
        }else if(targetJointAxis == 2){
            dirAxis = targetAxisZ;
        }else if(targetJointAxis == 3){
            dirAxis = -targetAxisX;
        }else if(targetJointAxis == 4){
            dirAxis = -targetAxisY;
        }else if(targetJointAxis == 5){
            dirAxis = -targetAxisZ;
        }
    }

    float   rotAngle        = acos(dot(dirAxis, mainAxis));
    vector  rotAxis         = normalize(cross(mainAxis, dirAxis));
    matrix3 rot             = qconvert(quaternion(rotAngle, rotAxis));
    jointTransform          *= rot;

    if(axisToLock > 0){

        if(axisToAlign == 0 || axisToAlign == 3){
            if(axisToLock == 2){
                axisY   = lockedAxis;
                axisZ   = normalize(cross(dirAxis, axisY));
                axisX   = normalize(cross(axisY, axisZ));
            }
            else if(axisToLock == 3){
                axisZ   = lockedAxis;
                axisY   = normalize(cross(axisZ, dirAxis));
                axisX   = normalize(cross(axisY, axisZ));
            }
            if(axisToAlign == 3){
                axisX = -axisX;
                axisZ = -axisZ;
            }

        }else if(axisToAlign == 1 || axisToAlign == 4){
            if(axisToLock == 1){
                axisX   = lockedAxis;
                axisZ   = normalize(cross(axisX, dirAxis));
                axisY   = normalize(cross(axisZ, axisX));
            }else if(axisToLock == 3){
                axisZ   = lockedAxis;
                axisX   = normalize(cross(dirAxis, axisZ));
                axisY   = normalize(cross(axisZ, axisX));
            }
            if(axisToAlign == 4){
                axisY = -axisY;
                axisX = -axisX;
            }
        }else if(axisToAlign == 2 || axisToAlign == 5){
            if(axisToLock == 1){
            axisX   = lockedAxis;
            axisY   = normalize(cross(dirAxis, axisX));
            axisZ   = normalize(cross(axisX, axisY));

            }else if(axisToLock == 2){
                axisY   = lockedAxis;
                axisX   = normalize(cross(axisY, dirAxis));
                axisZ   = normalize(cross(axisX, axisY));
            }
            if(axisToAlign == 5){
                axisZ = -axisZ;
                axisY = -axisY;
            }
        }

        vectorToMatrix(axisX, axisY, axisZ, jointTransform);
    }

    setpointattrib(geoID, "transform", jointID, jointTransform);

}


#endif