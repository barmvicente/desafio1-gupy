# -*-encoding: UTF-8 -*-

from collections import namedtuple
from flask import Flask, request, abort
import re

main_tuple = ()


def sort_tuples(maintuple, array_of_tuples):
    """Função que recebe a tupla principal e uma array de tuplas, retorna uma
    array de tuplas ordenada tendo a tupla principal como parâmetro"""

    global main_tuple

    main_tuple = maintuple

    """Cria uma classe com os atributos tupla recebida e a diferença entre a
    recebida e a tupla principal"""
    SortTuple = namedtuple('SortTuple', ['tuple_received', 'dif_tuple'])

    #Objeto que recebe a array de tuplas e calcula a chave de ordenação
    tuples_object = [SortTuple(x, key_sorted(x)) for x in array_of_tuples]

    """Uso de função sorted que usa como parâmetro a diferença entre as tuplas
    e a principal"""
    sorted_tuples = sorted(tuples_object, key=lambda x: x.dif_tuple)

    #array de tuplas ordenadas
    result = [x.tuple_received for x in sorted_tuples]

    return result


def key_sorted(tuple_received):
    """ Função que recebe uma tupla e calcula a diferença espacial entre esta
    e a tupla principal """

    global main_tuple

    size_tuples = len(main_tuple)
    array_dif_tuple = []

    #Montagem de array de diferenças
    for i in range(size_tuples):
        array_dif_tuple.append(abs(tuple_received[i] - main_tuple[i]))

    #Calculo da distância espacial
    return (sum(map(lambda x: x**2, (array_dif_tuple))))**(0.5)


app = Flask(__name__)


@app.route('/<string:maintuple>/<string:array_of_tuples>')
def index(maintuple, array_of_tuples):
    """Função que recebe a requisição do usuário e retorna uma array de tuplas
    ordenada de acordo com a tupla principal, casa haja um erro, a função
    retornará um HTTP 400"""

    try:
        maintuple = map(int, maintuple[1:-1].split(','))
        array_of_tuples = array_of_tuples[1:-1].split('),')
        arr = []
        for i in range(len(array_of_tuples)):
            tuples = re.findall(r'\d', array_of_tuples[i])
            tuples = map(int, tuples)
            arr.append(tuple(tuples))

        sorted_tuples = [str(i) for i in sort_tuples(maintuple, arr)]

        return ', '.join(sorted_tuples).replace('u', '')
    except:
        return abort(400)


if __name__ == '__main__':
    app.run(debug=True)
