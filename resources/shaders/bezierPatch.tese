#version 410 core
layout(quads) in;

//Transformation input
uniform mat4 Model;
uniform mat4 View;
uniform mat4 Projection;

//Light input
uniform vec3 lightPos;

//Light output
out vec3 normal;
out vec3 FragPos;
out vec3 LightPos;
//Texture coordinate output
out vec2 textureCoord;
float Berstern(int i,float u)
{
    vec4 c=vec4(1,3,3,1);
    return c[i]*pow(u,i)*pow(1-u,3-i);
}
vec4 ComputeCubicBezier(float u,vec4 p0,vec4 p1,vec4 p2,vec4 p3){
    // Cubic Bezier interpolation
    vec4 p=Berstern(0,u)*p0+Berstern(1,u)*p1+Berstern(2,u)*p2+Berstern(3,u)*p3;
    return p;
}
vec3 dUBezier(float u,float v)
{
    vec3 vCurve[4];
    for (int j=0;j<4;++j)
    {
        vec4 p0=gl_in[j].gl_Position;
        vec4 p1=gl_in[j+4].gl_Position;
        vec4 p2=gl_in[j+8].gl_Position;
        vec4 p3=gl_in[j+12].gl_Position;
        vCurve[j]=ComputeCubicBezier(v,p0,p1,p2,p3).xyz;
    }
    return -3 * (1 - u) * (1 - u) * vCurve[0] +
       (3 * (1 - u) * (1 - u) - 6 * u * (1 - u)) * vCurve[1] +
       (6 * u * (1 - u) - 3 * u * u) * vCurve[2] +
       3 * u * u * vCurve[3];
}
vec3 dVBezier(float u,float v)
{
    vec3 uCurve[4];
    for (int j=0;j<4;++j)
    {
        vec4 p0=gl_in[j*4].gl_Position;
        vec4 p1=gl_in[j*4+1].gl_Position;
        vec4 p2=gl_in[j*4+2].gl_Position;
        vec4 p3=gl_in[j*4+3].gl_Position;
        uCurve[j]=ComputeCubicBezier(u,p0,p1,p2,p3).xyz;
    }
    return -3 * (1 - v) * (1 - v) * uCurve[0] +
       (3 * (1 - v) * (1 - v) - 6 * v * (1 - v)) * uCurve[1] +
       (6 * v * (1 - v) - 3 * v * v) * uCurve[2] +
       3 * v * v * uCurve[3];
}
void main()
{
    vec4 p=vec4(0);
    // The tessellation u coordinate
    float u =gl_TessCoord.x;
    float v=gl_TessCoord.y;
    for (int j=0;j<4;++j)
    {
        vec4 p0=gl_in[j*4].gl_Position;
        vec4 p1=gl_in[j*4+1].gl_Position;
        vec4 p2=gl_in[j*4+2].gl_Position;
        vec4 p3=gl_in[j*4+3].gl_Position;
        p+=Berstern(j,v)*ComputeCubicBezier(u,p0,p1,p2,p3);
    }
    //Normal vector on each vertices
    vec3 dU=dUBezier(u,v);
    vec3 dV=dVBezier(u,v);
    vec3 Normal=normalize(cross(dU,dV));
    normal = mat3(transpose(inverse(Model))) * Normal;
    //Vertices coordinate in View space(Used for light calculation)
    FragPos = vec3(View *Model*p);
    //Light position in View space
    LightPos=vec3(View * vec4(lightPos, 1.0));
    //Texture coordinate
    textureCoord=vec2(u,v);
    //Fragment position in Projection space
    gl_Position = Projection*View*Model*p;

}
