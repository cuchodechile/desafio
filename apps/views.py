from django.shortcuts import render
from apps.forms import ContactoForm
import requests
import json


def contacto(request):
    if request.method=='POST':
        formulario = ContactoForm(request.POST)

        if formulario.is_valid():
            #print(request.POST)
            in_year  = request.POST['inicio_year']
            in_month = request.POST['inicio_month']
            in_day   = request.POST['inicio_day']
            fi_year  = request.POST['final_year']
            fi_month = request.POST['final_month']
            fi_day   = request.POST['final_day']

            #final=request.POST['final']
            indicador=request.POST['Indicador']
            if indicador == 'UF':
                response = requests.get('https://api.sbif.cl/api-sbifv3/recursos_api/uf/periodo/'+in_year+'/'+in_month+'/'+fi_year+'/'+fi_month+'?apikey=749f7901e2324c4780b419bbe5b1a1663ebb1686&formato=json&callback=despliegue')
                print(response)
            else:
                response = requests.get('https://api.sbif.cl/api-sbifv3/recursos_api/dolar/periodo/'+in_year+'/'+in_month+'/'+fi_year+'/'+fi_month+'?apikey=749f7901e2324c4780b419bbe5b1a1663ebb1686&formato=json&callback=despliegue')
            if response.status_code == 200:
                cadena= response.json()
                #TODO: falta parcial el json
                if indicador == 'UF':
                    valores=cadena['UFs']
                else:
                    valores=cadena['Dolares']
                #print (valores)
                
                ejex=""
                ejey=""
                i=0;
                maxi=0;
                maximo=0;
                diaMaximo =""
                minimo=10000000;
                diaMinimo =""
                suma=0;
                promedio=0;


                for item in valores:
                    #ejex+= '\'' +  item['Fecha'] + '\''
                    #ejey+= '\'' + item['Valor'] + '\''
                    aux_str=item['Valor'].replace(".","")
                    maxi=float(aux_str.replace(",","."))
                    if maxi > maximo:
                        maximo=maxi
                        diaMaximo = item['Fecha']
                    if maxi < minimo:
                        diaMinimo =item['Fecha']
                        minimo = maxi
                    suma+=maxi
                    ejex+=   item['Fecha'] 
                    ejey+=  item['Valor'] 
                    i=i+1
                    if  len(valores) > i:
                        ejex+=  '|'
                        ejey+=  '|'
                if i>0:
                    promedio=suma/i;
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXX" , len(valores))
                print(ejex)
                print(ejey)
                return render(request, 'home.html', {
                    'ejex':ejex,
                     'ejey':ejey,
                    'Indicador': indicador,
                    'valores': valores,
                    'maximo': maximo,
                    'promedio' :promedio,
                    'diaMaximo' :diaMaximo,
                    'diaMinimo': diaMinimo,
                    'minimo': minimo
                })
            else:
                return render(request, 'home.html', {
                    'tablaRs':"<p>Error </p>",
                    'Indicador': "Error"
                })
    else:
        formulario = ContactoForm()
        
        context = {'formulario': formulario}
        return render(request, 'inicio.html',context)


#def home(request):
#    response = requests.get('http://freegeoip.net/json/')
#    geodata = response.json()
#    return render(request, 'home.html', {
#        'ip': geodata['ip'],
#       'country': geodata['country_name']
#    })