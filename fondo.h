#ifndef FONDO_H
#define FONDO_H

#include <iostream>
#include "glew.h"
#include <GL/freeglut.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include "stb_image.h"
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "shader.h"
#include <vector>
#include <fstream>
using namespace std;
class Fondo
{
public:
  Shader *shader;
  unsigned int texture;
  unsigned int VBO, VAO, EBO;
  vector<float> vertices;
  vector<int> indices;
  void load_file(){
    string filename = "./vertex.txt";
    string filename2 = "./edges.txt";
    ifstream file,file2;
    file.open(filename.c_str(), ios::in);
    file2.open(filename2.c_str(), ios::in);
    float lectura;
    int cont = 0;
    while(!file.eof()){
      file >> lectura;
      if(cont!=2){
        lectura *=  32.0f / 320.0f;
        cont += 1;
      }else{
        cont=0;
      }

      vertices.push_back(lectura);
    }
    file.close();

    while (!file2.eof())
    {
      file2 >> lectura;
      indices.push_back(lectura);
    }
    file2.close();
  }
  Fondo(string shader_filename){
    load_file();
    cout << vertices.size() << endl;
    cout << indices.size() << endl;




    shader = new Shader((shader_filename + ".vs").c_str(), (shader_filename + ".fs").c_str());

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, vertices.size()*sizeof(float), &vertices[0], GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.size() * sizeof(float), &indices[0], GL_STATIC_DRAW);

    // position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void *)0);
    glEnableVertexAttribArray(0);

    //color
  }
  void draw(glm::mat4 projection, glm::mat4 view, glm::mat4 matrix_model)
  {
    //fondo1
    glBindTexture(GL_TEXTURE_2D, texture);

    // render container
    shader->use();
    shader->setVec3("color", glm::vec3(255.0f, 0.0f, 0.0f));
    shader->setMat4("matrix_model", matrix_model);
    shader->setMat4("matrix_view", view);
    shader->setMat4("matrix_projection", projection);
    glBindVertexArray(VAO);
    glDrawElements(GL_TRIANGLES, indices.size(), GL_UNSIGNED_INT, 0);
  }
};
#endif
