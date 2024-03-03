#ifndef __FRANKENSTEIN_CONSTRUCTION_PLANE__
#define __FRANKENSTEIN_CONSTRUCTION_PLANE__

#include <frankenstein_skeletonConstants.h>

void
transformPlane(
    const int pointID
)
{
    int     jointID         = chi(sprintf("../%s", PPROJECTION_PLANE_ORIGIN));
    int     orient          = chi(sprintf("../%s", PPROJECTION_PLANE_ORIENT));
    vector  offsetPos       = chv(sprintf("../%s", PPROJECIONT_PLANE_OFFSETPOS));
    vector  offsetRot       = chv(sprintf("../%s", PPROJECIONT_PLANE_OFFSETROT));
    vector  offsetScl       = chv(sprintf("../%s", PPROJECIONT_PLANE_OFFSETSCL));
    float   scale           = chf(sprintf("../%s", PPROJECTION_PLANE_SCALE));
    vector  color           = chv(sprintf("../%s", PCOLOR_PLANE));

    vector  skinGeoCenter   = detail(1, ATTRIB_SKINGEO_CENTER);
    float   skinGeoSize     = detail(1, ATTRIB_SKINGEO_SIZE);

    setdetailattrib(0, "temp", orient);

    // Convert rotation euler to quaternion and then to matrix.
    vector4 rot             = eulertoquaternion(offsetRot, 0);
    // Convert to matrix 4.
    matrix  offsetMatrix    = matrix(qconvert(rot));
    // Set Offset matrix position.
    offsetMatrix.ax         = offsetPos.x;
    offsetMatrix.ay         = offsetPos.y;
    offsetMatrix.az         = offsetPos.z;
    // Set Offset matrix scale.
    offsetMatrix.xx         *= offsetScl.x;
    offsetMatrix.xy         *= offsetScl.x;
    offsetMatrix.xz         *= offsetScl.x;

    offsetMatrix.yx         *= offsetScl.y;
    offsetMatrix.yy         *= offsetScl.y;
    offsetMatrix.yz         *= offsetScl.y;
    
    offsetMatrix.zx         *= offsetScl.z;
    offsetMatrix.zy         *= offsetScl.z;
    offsetMatrix.zz         *= offsetScl.z;

    // Define the origin matrix.
    matrix originMatrix     = ident();
    // Center the origin matrix to skin geometry center.
    originMatrix.ax = skinGeoCenter.x;
    originMatrix.ay = skinGeoCenter.y;
    originMatrix.az = skinGeoCenter.z;

    if(orient == 0){
        originMatrix.az = 0;  
    }else if(orient == 1){
        originMatrix.ax = 0;
    }else{
        originMatrix.ay = 0;
    }

    // Use a joint as plane origin if the joint ID is not -1.
    if(jointID > -1){
        vector  jointPos    = point(2, "P", jointID);
        matrix3 jointTrans  = point(2, ATTRIB_TRANSFORM, jointID);
        originMatrix        = matrix(jointTrans);
        originMatrix.ax     = jointPos.x;
        originMatrix.ay     = jointPos.y;
        originMatrix.az     = jointPos.z;
    }

    vector pointPos = point(0, "P", pointID);
    pointPos        = pointPos * skinGeoSize * scale * offsetMatrix * originMatrix;

    setpointattrib(0, "P", pointID, pointPos);
    setpointattrib(0, "Cd", pointID, color);

}




#endif