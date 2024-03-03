#ifndef __FRANKENSTEIN_PROJECTION_TOOLS__
#define __FRANKENSTEIN_PROJECTION_TOOLS__

int
projectionFree(
    const int       geoID;
    const int       pointID;
    const vector    rayOrigin;
    const vector    rayDirection;
    export vector   pointPos
)
{
    if(pointID > -1){
        pointPos            = point(geoID, "P", pointID);
        vector pointDist    = length(pointPos - rayOrigin);
        pointPos            = rayDirection * pointDist + rayOrigin;
        return 1;
    }
    return 0;
}

int
projectionSurface(
    const int       surfaceGeoID;
    const vector    rayOrigin;
    const vector    rayDirection;
    const float     maxDist;
    const int       snapPoint;
    const int       surfacePointID;
    export vector   pointPos
)
{
    if(snapPoint == 1){
        if(surfacePointID > -1){
            pointPos = point(surfaceGeoID, "P", surfacePointID);
            return 1;
        }
    }

    vector hitPos, hitUVW;
    int hitID = intersect(
        surfaceGeoID, 
        rayOrigin,
        rayDirection * maxDist,
        hitPos,
        hitUVW);
    pointPos = hitPos;
    if(hitID > -1){
        return 1;
    }
    return 0;
}

int
projectionSurfaceDepth(
    const int       surfaceGeoID;
    const int       rayType;
    const vector    rayOrigin;
    const vector    rayDirection;
    const float     mixFrontBack;
    const float     maxDist;
    const int       snapPoint;
    const int       sufacePointID;
    const int       depthType;
    export vector   pointPos;
)
{
    vector rayOrig = rayOrigin;
    vector rayDir  = rayDirection * maxDist;

    if(snapPoint == 1){
        if(sufacePointID > -1){
            rayOrig = point(surfaceGeoID, "P", sufacePointID);
            if(rayType == 1){
                rayDir  = point(surfaceGeoID, "N", sufacePointID);
                rayDir  = rayDir * -1 * maxDist;
            }
        }
    }else{
        if(rayType == 1){
            vector  hitPos, hitUV;
            int hitID = intersect(surfaceGeoID, rayOrigin, rayDirection*maxDist, hitPos, hitUV);
            if(hitID > -1){
                rayOrig = hitPos;
                rayDir = primuv(surfaceGeoID, "N", hitID, hitUV);
                rayDir = rayDir * -1 * maxDist;
            }
        }
    }

    int     hitIDs[];
    vector  hitPositions[];
    vector  hitUVWs[];

    int     hitCount = intersect_all(
        surfaceGeoID, 
        rayOrig, 
        rayDir,
        hitPositions,
        hitIDs,
        hitUVWs);
    
    if(depthType == 0){
        if(hitCount >= 2){
            pointPos = hitPositions[0] + (hitPositions[1] - hitPositions[0]) * mixFrontBack;
            return 1;
        }
    }else if(depthType == 1){
        if(hitCount >= 2){
            pointPos = hitPositions[0] + (hitPositions[-1] - hitPositions[0]) * mixFrontBack;
            return 1;
        }    
    }

    return 0;
}

int
projectionPosition(
    const int       geoID;
    const int       constructionGeoID;
    const int       surfaceGeoID;
    const int       pointID;
    const int       snapType;
    const float     mixFrontBack;
    const vector    rayOrigin;
    const vector    rayDirection;
    const int       snapPoint;
    const int       surfacePointID;
    const int       rayType;
    const int       depthType;
    export vector   pointPosition
){
    if(snapType == 0){
        return projectionFree(
            geoID, 
            pointID, 
            rayOrigin, 
            rayDirection, 
            pointPosition);
    }else if(snapType == 1){
        return projectionSurface(
            constructionGeoID, 
            rayOrigin, 
            rayDirection,
            1000.0,
            0,
            -1,
            pointPosition);
    }else if(snapType == 2){
        return projectionSurface(
            surfaceGeoID, 
            rayOrigin, 
            rayDirection, 
            1000.0,
            snapPoint,
            surfacePointID,
            pointPosition);
    }else if(snapType == 3){
        return projectionSurfaceDepth(
            surfaceGeoID, 
            rayType,
            rayOrigin, 
            rayDirection,
            mixFrontBack,
            1000.0,
            snapPoint,
            surfacePointID,
            depthType,
            pointPosition);
    }

    return 0;
}






#endif