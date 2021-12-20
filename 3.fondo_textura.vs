#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 matrix_model;
uniform mat4 matrix_view;
uniform mat4 matrix_projection;

uniform vec3 color;
out vec3 ourColor;

void main()
{
  mat4 mvp = matrix_projection * matrix_view * matrix_model;

  gl_Position = mvp * vec4(aPos, 1.0);
	ourColor = color;
}
