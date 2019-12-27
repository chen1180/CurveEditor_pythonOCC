#version 410 core

layout (location = 0) in vec3 Position_VS_in;
void main()
{
    gl_Position = vec4(Position_VS_in, 1.0);
}
