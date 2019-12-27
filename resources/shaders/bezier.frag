#version 410 core

out vec4 FragColor;
uniform vec3 objectColor;
uniform vec3 lightColor;
void main()
{
    //Ambient light
    float ambientStrength=1.0;
    vec3 ambient=ambientStrength*lightColor;
    vec3 result=ambient*objectColor;
    FragColor = vec4(result,1.0);

}
