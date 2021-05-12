from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
# from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework import status
from decimal import Decimal
from django.db.models import Count, Avg, Sum
from django.db.models import Q, F

# Create your views here.


@api_view(['GET', 'POST'])
def product_list(request, domainname):
    mt_id = _getmt(domainname)
    if request.method == 'GET':
        product_list = Product.objects.all()
        serializer = ProductSerializer(product_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)
    elif request.method == 'POST':
        data = request.data
        data['mt'] = mt_id
        serializer = NuggetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def product_detail(request, product_id, domainname):
    # product is zweckentfremded für nuggets
    # here we dont need a domain becuase the usere only recieves his own maybe implement for addational security a check
    # TODO implement check if this nugget belongs to the domain
    try:
        nugget = Nugget.objects.get(pk=product_id)
    except Nugget.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = NuggetSerializer(nugget, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        nugget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def cat_list(request, domainname):
    mt_id = _getmt(domainname)
    if request.method == 'GET':
        cat_list = Cat.objects.all().distinct('cat0').filter(mt_id=mt_id)
        serializer = CatSerializer(cat_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)
    elif request.method == 'POST':
        # implement filtering
        # serializer = CatSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        selected_cat = data.get('selectedCat')
        cat_level = data.get('catLevelRequested')
        if cat_level == 1:
            if selected_cat == 'all':
                cat_list = Cat.objects.all().distinct('cat1').filter(mt_id=mt_id)
            else:
                cat_list = Cat.objects.all().filter(cat0=selected_cat, mt_id=mt_id).distinct('cat1')
        elif cat_level == 2:
            cat_list = Cat.objects.all().filter(cat1=selected_cat, mt_id=mt_id).distinct('cat2')
        serializer = CatSerializer(cat_list, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def nugget_list(request, domainname):
    mt_id = _getmt(domainname)
    if request.method == 'GET':
        nu_list = Nugget.objects.filter(active=True, mt_id=mt_id, addonflag=False)
        serializer = NuggetSerializer(nu_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)
    elif request.method == 'POST':
        # implement filtering
        data = request.data
        selected_cat = data.get('cat')
        cat_level = data.get('catLevel')
        if cat_level == 1:
            # selected_cat_des = selected_cat.get('cat0')
            if selected_cat.get('cat0') == 'all' or selected_cat.get('cat0') == 'All':
                cat_list = Nugget.objects.all().filter(active=True, mt_id=mt_id,  addonflag=False)
            else:
                cat_list = Nugget.objects.all().filter(nuggetcat__cat__cat0=selected_cat.get('cat0'),
                                                       active=True,
                                                       mt_id=mt_id,
                                                       addonflag=False
                                                       )
        elif cat_level == 2:
            selected_cat_des = selected_cat.get('cat1')
            cat_list = Nugget.objects.all().filter(nuggetcat__cat__cat1=selected_cat_des,
                                                   active=True,
                                                   mt_id=mt_id,
                                                   addonflag=False
                                                   )
        elif cat_level == 3:
            selected_cat_des = selected_cat.get('cat2')
            cat_list = Nugget.objects.all().filter(nuggetcat__cat__cat2=selected_cat_des,
                                                   active=True,
                                                   mt_id=mt_id,
                                                   addonflag=False
                                                   )
        serializer = NuggetSerializer(cat_list, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def nugget_list_all(request, domainname):
    mt_id = _getmt(domainname)
    if request.method == 'GET':
        cat_list = Nugget.objects.all().filter(mt_id=mt_id)
        serializer = NuggetSerializer(cat_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)


@api_view(['GET'])
def option_cat_list(request, domainname):
    mt_id = _getmt(domainname)
    if request.method == 'GET':
        option_ca_list = OptionCat.objects.all().filter(mt_id=mt_id)
        serializer = OptionCatSerializer(option_ca_list, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def addon_list(request, domainname):
    mt_id = _getmt(domainname)
    add_query = None
    return_list = list()
    if request.method == 'GET':
        add_query = Nugget.objects.values('pk', 'description', 'einzelpreis', 'menge',
                                          'optioncat', 'optioncat__description')\
            .filter(mt_id=mt_id, addonflag=True).order_by('optioncat')
        add_list = list(add_query)
        return_list = create_addon_list(add_list)
        return Response(return_list)
    elif request.method == 'POST':
        data = request.data
        nugget_id = data.get('nugget_id')
        try:
            # nugget = Nugget.objects.get(pk=nugget_id)
            # get the Cat the current Nugget belongs to
            nugget_cat = NuggetCat.objects.values('cat_id').get(mt_id=1, nugget_id=nugget_id)
            cat_id = nugget_cat.get('cat_id')
        except NuggetCat.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # TODO find a better way than to hard code throug model would be possible.. assign the cat to the
        # TODO options there should be an extra tablt CatOptionCat or smth like this
        # for now hard code should be ok
        # wenn cat id = 9 Salat return nothing
        if cat_id == 9 and mt_id == 1:
            pass
        # wenn cat id = 9 Pizza  return nothing
        elif cat_id == 8 and mt_id == 1:
            add_query = Nugget.objects.values('pk', 'description', 'einzelpreis', 'menge',
                                              'optioncat', 'optioncat__description')\
                .filter(mt_id=mt_id, addonflag=True).order_by('optioncat')\
                .exclude(Q(optioncat__pk=5))
        elif cat_id == 10 and mt_id == 1:
            add_query = Nugget.objects.values('pk', 'description', 'einzelpreis', 'menge',
                                              'optioncat', 'optioncat__description')\
                .filter(mt_id=mt_id, addonflag=True).order_by('optioncat')\
                .exclude(Q(optioncat__pk=3) | Q(optioncat__pk=4) | Q(optioncat__pk=2))
        if add_query:
            add_list = list(add_query)
            return_list = create_addon_list(add_list)
        return Response(return_list)


@api_view(['GET', 'PUT','DELETE'])
def basket_addon_edit(request, domainname, basket_id):
    mt_id = _getmt(domainname)
    try:
        basket = Basket.objects.get(pk=basket_id)
        group = basket.group
        folg_id = basket.folg_id
    except Basket.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # get all nuggets which ddepending on the nugget addons for current basket and set quantity from basket

        add_basket_list = Nugget.objects.values('pk', 'description', 'einzelpreis', 'menge',
                                                'optioncat', 'optioncat__description')\
            .filter(mt_id=mt_id, addonflag=True).order_by('optioncat')
        try:
            basket_list_lo = Basket.objects.values().filter(group=group, addonflag=True, folg_id=folg_id)
            for add_basket in add_basket_list:
                for basket_loop in basket_list_lo:
                    if add_basket.get('pk') == basket_loop.get('nugget_id'):
                        add_basket['menge'] = basket_loop['menge']
                        add_basket['value'] = basket_loop['value']
        except Basket.DoesNotExist:
            pass
        return_basket_list = create_addon_list(add_basket_list)
        return Response(return_basket_list)
    elif request.method == 'PUT':
        data = request.data
        new_menge = data.get('newMenge')
        remove_flag = data.get('removeFlag')
        if new_menge == 0:
            Basket.objects.filter(folg_id=folg_id, group=group).delete()
        else:
            einzelpreis = basket.value / basket.menge
            if remove_flag:
                new_value = basket.value - einzelpreis
            else:
                new_value = basket.value + einzelpreis
            Basket.objects.filter(folg_id=folg_id, group=group).update(menge=new_menge, value=new_value)
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'DELETE':
        Basket.objects.filter(folg_id=folg_id, group=group).delete()
        basket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def basket_list(request, domainname):
    mt_id = _getmt(domainname)
    if request.method == 'GET':
        basket_list = Basket.objects.filter(mt_id=mt_id)
        serializer = BasketSerializer(basket_list, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        data['mt'] = mt_id
        basket = Basket(**data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def basket_details(request, domainname, folg_id):
    mt_id = _getmt(domainname)
    try:
        folg = Folg.objects.get(pk=folg_id)
    except Folg.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # get a list of all addons as a string to display in table for each basket
        baskets = Basket.objects.values('pk',
                                        'description',
                                        'nugget_id',
                                        'menge',
                                        'value',
                                        'group',
                                        'note',
                                        'nugget__pic_url')\
            .filter(folg_id=folg_id, addonflag=False).order_by('pk')
        # serializer = BasketSerializer(baskets, context={'request': request}, many=True)
        for bask in baskets:
            add_str = ""
            addon_query = Basket.objects.values('nugget__description', 'menge')\
                .filter(folg_id=folg_id, group=bask.get('group'), addonflag=True)
            if addon_query:
                addon_loop_list = list(addon_query)
                for index, add in enumerate(addon_loop_list):
                    if index == len(addon_loop_list) - 1:
                        add_str += str(int(add.get('menge'))) + 'x' + add.get('nugget__description')
                    else:
                        add_str += str(int(add.get('menge'))) + 'x' + add.get('nugget__description') + ', '

            bask['addonString'] = add_str
        return Response(baskets)
    elif request.method == 'POST':
        data = request.data
        delete_flag = data.get('deleteFlag')
        update_note_flag = data.get('updateNoteFlag')
        group = data.get('group')
        if delete_flag:
            Basket.objects.filter(mt_id=mt_id, folg_id=folg_id, group=group).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif update_note_flag:
            note = data.get('anmerkung')
            basket_to_update = Basket.objects.get(mt_id=mt_id, folg_id=folg_id, group=group, addonflag=False)
            basket_to_update.note = note
            basket_to_update.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            parent_nugget_id = data.get('parent_nugget_id')
            nugget = data.get('nugget')
            group_id = nugget.get('group')
            nugget['mt_id'] = mt_id
            nugget['folg_id'] = folg_id
            nugget['value'] = nugget.get('einzelpreis')
            # nugget['value'] = nugget.get('einzelpreis')
            # get parent in basket to add one addoncount
            basket_nugget = Basket.objects.get(nugget_id=parent_nugget_id, group=group_id, mt_id=mt_id)
            addon_basket = Basket.objects.create(**nugget)
            if addon_basket:
                current_addon_count = basket_nugget.addonCount
                if current_addon_count is None:
                    current_addon_count = 0
                cur_value = basket_nugget.value
                if cur_value is None:
                    cur_value = basket_nugget.einzelpreis
                    # need to check the correct value
                cur_value = Decimal(cur_value) + Decimal(addon_basket.einzelpreis)
                basket_nugget.value = cur_value
                current_addon_count += 1
                basket_nugget.addonCount = current_addon_count
                basket_nugget.save()
                return Response({'newNuValue': cur_value}, status=status.HTTP_201_CREATED)
            return Response('error while adding nugget to basket', status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        data = request.data
        parent_nugget_id = data.get('parent_nugget_id')
        nugget = data.get('nugget')
        group_id = nugget.get('group')
        new_menge = nugget.get('menge')
        nugget_id = nugget.get('nugget_id')
        nugget_basket = Basket.objects.get(nugget_id=parent_nugget_id, group=group_id, mt_id=mt_id)
        addon_basket = Basket.objects.get(nugget_id=nugget_id, group=group_id, folg_id=folg_id)
        # check if + or -
        menge_diff = new_menge - addon_basket.menge
        cur_value = nugget_basket.value
        cur_addon_value = addon_basket.value
        addon_count = nugget_basket.addonCount
        # if cur_value is None:
        # cur_value = 0
        if cur_addon_value is None:
            cur_addon_value = addon_basket.einzelpreis
        if menge_diff < 0:
            # need to remove one addon
            cur_addon_value = Decimal(cur_addon_value) - Decimal(nugget.get('einzelpreis'))
            cur_value = Decimal(cur_value) - Decimal(nugget.get('einzelpreis'))
            addon_count -= 1
        else:
            cur_addon_value = Decimal(cur_addon_value) + Decimal(nugget.get('einzelpreis'))
            cur_value = Decimal(cur_value) + Decimal(nugget.get('einzelpreis'))
            addon_count += 1
            # need to add one
        # TODO check if we want to count the no of addons including quantity or not
        nugget_basket.addonCount = addon_count
        nugget_basket.value = cur_value
        if new_menge == 0:
            # delete that item
            addon_basket.delete()
        else:
            # value can also be calculated with new menge * einzelpreis
            addon_basket.menge = new_menge
            addon_basket.value = cur_addon_value
            addon_basket.save()
        nugget_basket.save()
        return Response({'newNuValue': cur_value}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT'])
def folg_list(request, domainname):
    mt_id = _getmt(domainname)
    if request.method == 'GET':
        folg_list_query = Folg.objects.filter(mt_id=mt_id)
        serializer = FolgSerializer(folg_list_query, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        group_id = 1
        data = request.data
        nugget = data.get('nugget')
        folg_id = data.get('cartId')
        nugget['mt_id'] = mt_id
        # create Folg with status initial if there is no cartID
        if folg_id is None:
            new_folg = Folg.objects.create(mt_id=mt_id, status_id=1, counter=1)
            if new_folg:
                folg_id = new_folg.pk
            else:
                return Response('cannot create new Folg', status=status.HTTP_400_BAD_REQUEST)
        else:
            # get the number of nuggets added in this folg
            folg_query = Folg.objects.get(pk=folg_id)
            group_id = folg_query.counter
            # TODO check if a check is needed for addational adding or not
            # add one to counter
            group_id += 1
            folg_query.counter = group_id
            folg_query.save()
        nugget['folg_id'] = folg_id
        nugget['group'] = group_id
        nugget['addonCount'] = 0
        # TODO maybe add anotherone  if menge is already 1 ????
        nugget['menge'] = 1
        nugget['value'] = nugget.get('einzelpreis')
        basket = Basket(**nugget).save()
        return Response({'cartId': folg_id, 'group': group_id}, status=status.HTTP_201_CREATED)
        # return Response('cannot create new Folg', status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        # create Pair and change status of folg
        # set pair in folg set status to completed set payment method
        data = request.data
        folg_id = data.get('cartId')
        try:
            folg = Folg.objects.get(pk=folg_id, mt_id=mt_id)
        except Folg.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        method_id = data.get('methodId')
        pair_info = data.get('details')
        paymentInfo = data.get('paymentinfo')
        pair_info['mt_id'] = mt_id
        new_pair = Pair.objects.create(**pair_info)
        folg.pair = new_pair
        # TODO check if completed is the right status
        folg.status_id = 3
        folg.method_id = method_id
        folg.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def basket_count(request, domainname, folg_id):
    mt_id = _getmt(domainname)
    if request.method == 'GET':
        count_bas = Basket.objects.filter(mt_id=mt_id, folg_id=folg_id, addonflag=False).count()
        return Response(count_bas)


@api_view(['GET'])
def folg_total(request, domainname, folg_id):
    mt_id = _getmt(domainname)
    if request.method == 'GET':
        sum_folg = Basket.objects.filter(mt_id=mt_id, folg_id=folg_id, addonflag=False)\
            .aggregate(value_sum=Sum('value'))
        return Response(sum_folg.get('value_sum'))


def create_addon_list(add_list):
    return_list = list()
    option_list = list()
    prev_option = None
    for index, add in enumerate(add_list):
        if prev_option:
            # nachfolgende durchläufe checke ob pre_option gleich aktueller option wenn ja append to optionlist
            if prev_option == add.get('optioncat'):
                option_list.append(add)
                prev_option = add.get('optioncat')
                prev_desc = add.get('optioncat__description')
            else:
                return_list.append({'description': prev_desc,
                                    'nuggets': option_list})
                option_list = list()
                option_list.append(add)
                prev_option = add.get('optioncat')
                prev_desc = add.get('optioncat__description')
        else:
            # erster durchlauf hänge ersten eintrag an option
            option_list.append(add)
            prev_option = add.get('optioncat')
            prev_desc = add.get('optioncat__description')
        if index == len(add_list) - 1:
            if len(option_list) == 0:
                option_list.append(add)
            return_list.append({'description': add.get('optioncat__description'),
                                'nuggets': option_list})
    return return_list


def _getmt(domain_name):
    domain = Domain.objects.values().get(name=domain_name)
    # TODO check if we need exception handling here always one to one? one Damain can only have one mt???
    if domain:
        return domain.get('mt_id')
