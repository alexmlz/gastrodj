from datetime import datetime, date, timedelta
from .models import Asys, AiSysDate, Atermin
import pytz
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist


today = date.today()
today_day = today.day
today_month = today.month
today_year = today.year


def createasys(sys_cp_id, sys_mt_id, utaint_id):
    """create new asys entry in the db"""
    today = datetime.today()
    cur_month = today.month
    if 1 <= cur_month <= 3:
        sys_period = 'q1'
    elif 4 <= cur_month <= 6:
        sys_period = 'q2'
    elif 7 <= cur_month <= 9:
        sys_period = 'q3'
    elif 10 <= cur_month <= 12:
        sys_period = 'q4'
    new_as = Asys(sys_cp_id=sys_cp_id, sys_mt_id=sys_mt_id,
                  period=sys_period, utaint_id=utaint_id, status='offen')
    new_as.save()
    return new_as.id


def increasetmsp(aisysdate_obj, end_hour):
    beginn_tmsp = aisysdate_obj.get('d_beginn_tmsp')
    end_tmsp = aisysdate_obj.get('d_end_tmsp')
    beginn_tmsp = beginn_tmsp.replace(hour=end_hour)
    new_end_hour = end_hour + 1
    end_tmsp = end_tmsp.replace(hour=new_end_hour)
    aisysdate_obj['d_beginn_hour'] = end_hour
    aisysdate_obj['d_end_hour'] = new_end_hour
    aisysdate_obj['d_beginn_tmsp'] = beginn_tmsp
    aisysdate_obj['d_end_tmsp'] = end_tmsp
    return aisysdate_obj


def createweeknormal(aisysdate_obj, late):
    # 10 - 11
    asys_id = createasys(1, 1, 1)
    aisysdate_obj['asys_id'] = asys_id
    new_aisys = AiSysDate(**aisysdate_obj)
    new_aisys.save()
    new_atermin = Atermin(asys_id=asys_id)
    new_atermin.save()
    # 11 -12
    asys_id = createasys(1, 1, 1)
    aisysdate_obj['asys_id'] = asys_id
    aisysdate_obj = increasetmsp(aisysdate_obj, aisysdate_obj['d_end_hour'])
    new_aisys = AiSysDate(**aisysdate_obj)
    new_aisys.save()
    new_atermin = Atermin(asys_id=asys_id)
    new_atermin.save()
    aisysdate_obj = increasetmsp(aisysdate_obj, aisysdate_obj['d_end_hour'])
    # 12 - 13
    asys_id = createasys(1, 1, 1)
    aisysdate_obj['asys_id'] = asys_id
    new_aisys = AiSysDate(**aisysdate_obj)
    new_aisys.save()
    new_atermin = Atermin(asys_id=asys_id)
    new_atermin.save()
    aisysdate_obj = increasetmsp(aisysdate_obj, aisysdate_obj['d_end_hour'])
    # 13 - 14
    asys_id = createasys(1, 1, 1)
    aisysdate_obj['asys_id'] = asys_id
    new_aisys = AiSysDate(**aisysdate_obj)
    new_aisys.save()
    new_atermin = Atermin(asys_id=asys_id)
    new_atermin.save()
    if late:
        aisysdate_obj = increasetmsp(aisysdate_obj, 18)
        # aisysdate_obj['d_beginn_hour'] = 18
        # aisysdate_obj['d_end_hour'] = 19
        # 13 - 14
        asys_id = createasys(1, 1, 1)
        aisysdate_obj['asys_id'] = asys_id
        new_aisys = AiSysDate(**aisysdate_obj)
        new_aisys.save()
        new_atermin = Atermin(asys_id=asys_id)
        new_atermin.save()


def createaisysdate(single_date):
    start_hour = 10
    end_hour = 11
    minutes = 00
    seconds = 00
    mm = 0
    beginn_day = single_date.day
    beginn_month = single_date.month
    beginn_year = single_date.year
    single_date_tmsp_beginn = datetime(beginn_year, beginn_month, beginn_day, start_hour, minutes, seconds, mm, pytz.UTC)
    single_date_tmsp_end = datetime(beginn_year, beginn_month, beginn_day, end_hour, minutes, seconds, mm, pytz.UTC)
    weekday = single_date.weekday()
    aisysdate_obj = {
                     'zeitraum': 'zeitraum',
                     'datum_type': 'termin',
                     'd_beginn_tmsp': single_date_tmsp_beginn,
                     'd_beginn_item_day': beginn_day,
                     'd_beginn_item_month': beginn_month,
                     'd_beginn_item_year': beginn_year,
                     'd_end_tmsp': single_date_tmsp_end,
                     'd_end_item_day': beginn_day,
                     'd_end_item_month': beginn_month,
                     'd_end_item_year': beginn_year,
                     'd_beginn_hour': start_hour, 'd_beginn_minute': minutes,
                     'd_end_hour': end_hour, 'd_end_minute': minutes}
    # 1 und 2 10 - 11 11 - 12 12 - 13 13 - 14
    # 3 4 und 5 10 - 11, 11 - 12, 13 - 14,  18-19
    if weekday == 1 or weekday == 2:
        createweeknormal(aisysdate_obj, False)
    if 2 < weekday < 6:
        createweeknormal(aisysdate_obj, True)
    return True


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def createappointment(start, end):
    beginn_obj = date.fromisoformat(start)
    end_obj = date.fromisoformat(end)
    for single_date in daterange(beginn_obj, end_obj):
        createaisysdate(single_date)
    return 'success'


def getappointments(agent_id, public):
    if public:
        data = AiSysDate.objects.filter(asys__sys_mt=agent_id, asys__status='offen').values()
    else:
        data = AiSysDate.objects.filter(asys__sys_mt=agent_id).values()
    for da in data:
        as_id = da.get('asys_id')
        asys_data = Asys.objects.get(id=as_id)
        try:
            atermindata = Atermin.objects.get(asys_id=as_id)
            atermin_dic = model_to_dict(atermindata)
            del atermin_dic['asys']
            da.update(atermin_dic)
        except ObjectDoesNotExist:
            pass
        asys_dic = model_to_dict(asys_data)
        del asys_dic['id']
        da.update(asys_dic)
    if data:
        data_for_return = {
                'fields': list(data[0].keys()),
                'data': data
            }
    else:
        data_for_return = {
                'fields': list(),
                'data': data
            }
    return data_for_return


def deleteAppointment(asys_id, aidate_id):
    atermin_data = Atermin.objects.get(asys_id=asys_id)
    a_name = atermin_data.name
    if a_name:
        return 'bereits gebuchter Termin kann nicht gelöscht werden'
    rowsaffected1 = AiSysDate.objects.filter(id=aidate_id).delete()
    rowsaffected = Asys.objects.filter(id=asys_id).delete()
    rowsaffected2 = Atermin.objects.filter(asys_id=asys_id)
    if rowsaffected1[0] + rowsaffected[0] + rowsaffected2[0] >= 3:
        return 'deleted'


def bookappointment(inputs, asys_id):
    new_atermin = dict()
    for inp in inputs:
        in_name = inp.get('name')
        if in_name == 'betreff':
            new_atermin['thema_item'] = inp.get('value')
        else:
            new_atermin[in_name] = inp.get('value')
    atermin = Atermin.objects.filter(asys_id=asys_id).update(**new_atermin)
    if atermin:
        asys = Asys.objects.get(id=asys_id)
        asys.status = 'booked'
        asys.save()
    return 'updated'




