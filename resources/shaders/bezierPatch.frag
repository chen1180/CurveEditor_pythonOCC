#version 410 core

uniform vec3 objectColor;
uniform vec3 lightColor;
uniform vec3 viewPos;
uniform bool wireFrameMode;
uniform sampler2D texture0;

in vec3 normal;
in vec3 FragPos;
in vec3 LightPos;
in vec2 textureCoord;

out vec4 FragColor;
void main()
{
    //Ambient light
    float ambientStrength=1.0;
    vec3 ambient=ambientStrength*lightColor;
    //     vec3 result = ambient* objectColor;
    //Diffuse light
    vec3 lightDir=normalize(LightPos-FragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    //Specular light
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;
    vec3 result=vec3(0);
//    vec3 result = (ambient + diffuse+specular)*texture2D(texture0,textureCoord).rgb*objectColor;
    if (wireFrameMode==true)
        result = objectColor;
    else
        result = ambient*objectColor;
    FragColor = vec4(result,1.0);
}
