#version 410 core
//define the maximum vertices point that can process
#define MAX_KNOTS 16
layout(quads) in;
//The dynamic array is not support in 4.1 glsl version, constant must be passed into array.
uniform float knots[MAX_KNOTS];
uniform float weights[MAX_KNOTS];
uniform int knots_size;
uniform int order;
uniform bool clamped;
uniform mat4 MVP;
//compute coefficient
void basicFunction(float u,int k,int p,inout float N[MAX_KNOTS]){
    //u: step (0~1)
    //k: step position in knots vector
    //p: order of the curve
    if (clamped==true){
        if (u==1.0){
            N[3]=1.0;
            return;
        } else if(u==0.0){
            N[0]=1.0;
            return;
        }
    }
    N[k] = 1.0;
    for(int d=1;d<p+1;d++){
        N[k - d] = (knots[k + 1] - u) / (knots[k + 1] - knots[(k - d) + 1]) * N[(k - d) + 1];
        for(int i=k-d+1;i<k;i++){
            N[i] = (u - knots[i]) /(knots[i + d] - knots[i])* N[i] + (knots[i + d + 1] - u) / (knots[i + d + 1] - knots[i + 1]) * N[i + 1];
        }
        N[k] = (u - knots[k]) / (knots[k + d] - knots[k]) * N[k];
    }
}
int findKnotSpan(in float u){
    //find the knotspan of u in knots
    int k=0;
    for (int i=0;i<knots_size-1;i++){
        if ((u >= knots[i])&&(u < knots[i+1]))
        {
            k=i;
            break;
        }
    }
    return k;
}
vec3 computeNurbsPoint( int index,float u,  int p){
    int k=findKnotSpan(u);
    //Initialize N array
    float N[MAX_KNOTS];
    for (int i=0;i<knots_size;i++){
        N[i]=0;
    }
    //calculate value of N
    basicFunction(u, k, p, N);
    vec3 lastP=vec3(0);
    for(int i=0;i<4;i++){
        lastP+=gl_in[4*index+i].gl_Position.xyz*weights[i]*N[i];
    }
    float W=0;
    for(int i=0;i<4;i++)
    {
        W+=weights[i]*N[i];
    }
    lastP/=W;
    return lastP;
}

void main()
{
    // The tessellation u coordinate
    float u =gl_TessCoord.x;
    float v=gl_TessCoord.y;
    //order
    int p=order;
    //Discard all the points between [knots[p],knots[m-p-1]]
    if (clamped==false){
        if((u<knots[p])||(u>knots[knots_size-p-1]))
        return;
        if((v<knots[p])||(v>knots[knots_size-p-1]))
        return;
    }
    int k=findKnotSpan(v);
    //Initialize N array
    float Nv[MAX_KNOTS];
    for (int i=0;i<knots_size;i++){
        Nv[i]=0;
    }
    basicFunction(v, k, p, Nv);
    float Wv=0;
    for(int i=0;i<4;i++)
    {
        Wv+=weights[i]*Nv[i];
    }
    vec3 lastP=vec3(0.0);
    for (int j=0;j<4;++j)
    {
        lastP+=computeNurbsPoint(j,u,p)*Nv[j]*weights[j]/Wv;
    }
    gl_Position = MVP*vec4( lastP,1.0);
}