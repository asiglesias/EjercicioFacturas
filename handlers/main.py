#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from webapp2_extras import jinja2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("index.html"))

    def post(self):
        campos = ["cif", "nombre", "apellidos", "email", "direccion", "poblacion", "codpostal", "pais", "percontacto", "telefono"]
        dict = {}
        for campo in campos:
            dict[campo] = self.request.get(campo, "")
            dict[campo + "2"] = self.request.get(campo + "2", "")

        lineas = self.request.POST.getall("lineafactura")
        lineasfactura = []
        for linea in lineas:
            linea_dict = {}
            values = linea.split(';')
            linea_dict['concepto'] = values[0]
            linea_dict['numero'] = values[1]
            linea_dict['precio'] = values[2]
            linea_dict['porcentaje'] = values[3]
            linea_dict['importe'] = values[4]
            lineasfactura.append(linea_dict)

        dict["lineas"] = lineasfactura
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("factura.html", **dict))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/generarfactura', MainHandler)
], debug=True)
