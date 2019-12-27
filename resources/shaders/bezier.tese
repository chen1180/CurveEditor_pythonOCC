#version 410 core
#define MAX_KNOTS 32
layout(isolines) in;
//The dynamic array is not support in 4.1 glsl version, constant must be passed into array.
uniform mat4 MVP;
out vec3 tangent;
//compute coefficient
vec3 ComputeCubicBezier(float u,vec3 p0,vec3 p1,vec3 p2,vec3 p3){
    // The patch vertices (control points)
    float u1 = (1.0 - u);
    float u2 = u * u;
    // Bernstein polynomials evaluated at u
    float b3 = u2 * u;
    float b2 = 3.0 * u2 * u1;
    float b1 = 3.0 * u * u1 * u1;
    float b0 = u1 * u1 * u1;
    // Cubic Bezier interpolation
    return (p0 * b0 + p1 * b1 + p2 * b2 + p3 *b3);
}
//tangent vector of CubicBezierCurve
vec3 ComputeCubicBezierDerivative(float u,vec3 p0,vec3 p1,vec3 p2,vec3 p3){
    vec3 a=3*(p1-p0);
    vec3 b=3*(p2-p1);
    vec3 c=3*(p3-p2);
    return a * pow(1-u,2) + 2 * b * (1-u) * u + c * pow(u,2);
}
int factorial(int n) {
    int result = 1;
    for (int i = n; i > 1; i--)
    result *= i;
    return result;
}
float binomial_coefficient(int i, int n) {
  return 1.0f * factorial(n) / (factorial(i) * factorial(n-i));
}
float bernstein_polynomial(int i, int n, float u) {
  return binomial_coefficient(i, n) * float(pow(u, i)) * float(pow(1.0-u, n-i));
}
vec3 computeBezierPoint(float u){
    int n=gl_PatchVerticesIn;
    vec3 lastP=vec3(0.0,0.0,0.0);
    for(int i=0;i<n;i++){
        lastP+=gl_in[i].gl_Position.xyz*bernstein_polynomial(i, n-1, u);
    }
    return lastP;
}
void main()
{
    // The tessellation u coordinate
    float u = gl_TessCoord.x;
    vec3 p=computeBezierPoint(u);
    gl_Position = MVP*vec4(p,1.0);
}