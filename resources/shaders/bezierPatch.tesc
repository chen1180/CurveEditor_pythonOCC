#version 410 core

// define the number of CPs in the output patch
layout (vertices = 16) out;


void main()
{
    // Pass along the vertex position unmodified
        gl_out[gl_InvocationID].gl_Position =
        gl_in[gl_InvocationID].gl_Position;
       // Calculate the tessellation levels
       gl_TessLevelOuter[0] =20;
       gl_TessLevelOuter[1] = 20;
       gl_TessLevelOuter[2] =20;
       gl_TessLevelOuter[3] = 20;
        gl_TessLevelInner[0] =20;
       gl_TessLevelInner[1] = 20;
   }
