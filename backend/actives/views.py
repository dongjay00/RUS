from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Active, ActiveDetail
from users.models import User, Group
from .serializers import ActiveSerializer, ActiveDetailSerializer
from users.serializers import UserSerializer, GroupSerializer

from datetime import datetime, timedelta



def calculateTime(st, en):
    result = 0

    start = datetime(int(st[:4]), int(st[5:7]), int(st[8:10]), int(st[11:13]), int(st[14:16]), int(st[17:19]))
    end = datetime(int(en[:4]), int(en[5:7]), int(en[8:10]), int(en[11:13]), int(en[14:16]), int(en[17:19]))
    result += ((end - start).days * 24)
    result += ((end - start).seconds / 3600)
    return round(result, 2)
    
def caculateMaxDay(year_num, month_num):
    if month_num in ['01', '03', '05', '07', '08', '10', '12']:
        return 31
    elif month_num == '02':
        if int(year_num) % 4 == 0:
            if int(year_num) % 100 != 0:
                return 29
            else: 
                if int(year_num) % 400 == 0:
                    return 29
                else:
                    return 28
        else:
            return 28
    else:
        return 30



# Create your views here.
@api_view(['POST'])
def save_active(request):
    user_info = User.objects.get(pk=request.data["user_pk"])
    new_active = {
        "user": request.data["user_pk"],
        "start_time": request.data["start_time"],
        "end_time": request.data["end_time"],
    }
    a_serializer = ActiveSerializer(data=new_active)

    if a_serializer.is_valid(raise_exception=True):
        a_serializer.save()
    
    actives = Active.objects.all().order_by('-pk')[0]

    for i in request.data["active_details"]:
        new_active_detail = {
            "active": actives.id,
            "active_type": i["active_type"],
            "startTime": i["start_time"],
            "endTime": i["end_time"]
        }
        ad_serializer = ActiveDetailSerializer(data=new_active_detail)
        if ad_serializer.is_valid(raise_exception=True):
            ad_serializer.save()
    
    return Response(status=status.HTTP_201_CREATED)



@api_view(['GET'])
def get_my_timelines(request, user_pk):
    Actives = Active.objects.all().filter(user=user_pk)
    serializer = ActiveSerializer(Actives, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_active_detail_info(request, active_pk):
    Active_Detail = ActiveDetail.objects.all().filter(active=active_pk)
    serializer = ActiveDetailSerializer(Active_Detail, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_my_active(request, user_pk, search_type, start_date, end_date):

    Actives = Active.objects.all().filter(user=user_pk)
    Active_Detail = ActiveDetail.objects.all()

    result = []

    if search_type == 'year':

        result_jan = {
            "name": "1월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_feb = {
            "name": "2월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_mar = {
            "name": "3월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_apr = {
            "name": "4월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_may = {
            "name": "5월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_jun = {
            "name": "6월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_jul = {
            "name": "7월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_aug = {
            "name": "8월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_sep = {
            "name": "9월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_oct = {
            "name": "10월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_nov = {
            "name": "11월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        result_dec = {
            "name": "12월",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }

        for i in Actives:
            str_start_time = str(i.start_time)
            if str_start_time[:4] == start_date[:4]:
                # 1월
                if str_start_time[5:7] == '01':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_jan["studyTime"] += time
                        elif j.active_type == 0:
                            result_jan["restTime"] += time
                        else:
                            result_jan["otherTime"] += time
                # 2월
                elif str_start_time[5:7] == '02':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_feb["studyTime"] += time
                        elif j.active_type == 0:
                            result_feb["restTime"] += time
                        else:
                            result_feb["otherTime"] += time
                # 3월
                elif str_start_time[5:7] == '03':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_mar["studyTime"] += time
                        elif j.active_type == 0:
                            result_mar["restTime"] += time
                        else:
                            result_mar["otherTime"] += time
                # 4월
                elif str_start_time[5:7] == '04':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_apr["studyTime"] += time
                        elif j.active_type == 0:
                            result_apr["restTime"] += time
                        else:
                            result_apr["otherTime"] += time
                # 5월
                elif str_start_time[5:7] == '05':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_may["studyTime"] += time
                        elif j.active_type == 0:
                            result_may["restTime"] += time
                        else:
                            result_may["otherTime"] += time
                # 6월
                elif str_start_time[5:7] == '06':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_jun["studyTime"] += time
                        elif j.active_type == 0:
                            result_jun["restTime"] += time
                        else:
                            result_jun["otherTime"] += time
                # 7월
                elif str_start_time[5:7] == '07':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_jul["studyTime"] += time
                        elif j.active_type == 0:
                            result_jul["restTime"] += time
                        else:
                            result_jul["otherTime"] += time
                # 8월
                elif str_start_time[5:7] == '08':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_aug["studyTime"] += time
                        elif j.active_type == 0:
                            result_aug["restTime"] += time
                        else:
                            result_aug["otherTime"] += time
                # 9월
                elif str_start_time[5:7] == '09':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_sep["studyTime"] += time
                        elif j.active_type == 0:
                            result_sep["restTime"] += time
                        else:
                            result_sep["otherTime"] += time
                # 10월
                elif str_start_time[5:7] == '10':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_oct["studyTime"] += time
                        elif j.active_type == 0:
                            result_oct["restTime"] += time
                        else:
                            result_oct["otherTime"] += time
                # 11월
                elif str_start_time[5:7] == '11':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_nov["studyTime"] += time
                        elif j.active_type == 0:
                            result_nov["restTime"] += time
                        else:
                            result_nov["otherTime"] += time
                # 12월
                elif str_start_time[5:7] == '12':
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            result_dec["studyTime"] += time
                        elif j.active_type == 0:
                            result_dec["restTime"] += time
                        else:
                            result_dec["otherTime"] += time

        result.append(result_jan)
        result.append(result_feb)
        result.append(result_mar)
        result.append(result_apr)
        result.append(result_may)
        result.append(result_jun)
        result.append(result_jul)
        result.append(result_aug)
        result.append(result_sep)
        result.append(result_oct)
        result.append(result_nov)
        result.append(result_dec)

    elif search_type == 'month':
        start_date_year = start_date[:4]
        start_date_month = start_date[5:7]

        week1 = {
            "name": "01~07",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        week2 = {
            "name": "08~14",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        week3 = {
            "name": "15~21",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        week4 = {
            "name": "22~28",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        week5 = {
            "name": "29~",
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }

        max_day = caculateMaxDay(start_date_year, start_date_month)
        week5["name"] += str(max_day)

        for i in Actives:
            str_start_time = str(i.start_time)
            if str_start_time[:4] == start_date[:4] and str_start_time[5:7] == start_date[5:7]:
                if int(str_start_time[8:10]) <= 7:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            week1["studyTime"] += time
                        elif j.active_type == 0:
                            week1["restTime"] += time
                        else:
                            week1["otherTime"] += time
                elif 8 <= int(str_start_time[8:10]) <= 14:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            week2["studyTime"] += time
                        elif j.active_type == 0:
                            week2["restTime"] += time
                        else:
                            week2["otherTime"] += time
                elif 15 <= int(str_start_time[8:10]) <= 21:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            week3["studyTime"] += time
                        elif j.active_type == 0:
                            week3["restTime"] += time
                        else:
                            week3["otherTime"] += time
                elif 22 <= int(str_start_time[8:10]) <= 28:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            week4["studyTime"] += time
                        elif j.active_type == 0:
                            week4["restTime"] += time
                        else:
                            week4["otherTime"] += time
                else:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            week5["studyTime"] += time
                        elif j.active_type == 0:
                            week5["restTime"] += time
                        else:
                            week5["otherTime"] += time
        
        if max_day == 28:
            result.append(week1)
            result.append(week2)
            result.append(week3)
            result.append(week4)
        else:
            result.append(week1)
            result.append(week2)
            result.append(week3)
            result.append(week4)
            result.append(week5)

    elif search_type == 'week':
        start_date_year = start_date[:4]
        start_date_month = start_date[5:7]
        start_date_day = int(start_date[8:10])
        max_day = caculateMaxDay(start_date_year, start_date_month)
        
        
        info = [
            start_date_day, 
            start_date_day + 1,
            start_date_day + 2,
            start_date_day + 3,
            start_date_day + 4,
            start_date_day + 5,
            start_date_day + 6,
        ]

        for i in range(7):
            if info[i] > max_day:
                info[i] = (info[i] % max_day)
            info[i] = str(info[i])
            if len(info[i]) == 1:
                info[i] = '0' + info[i]

        day1 = {
            "name": start_date_month + '.' + info[0],
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        day2 = {
            "name": start_date_month + '.' + info[1],
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        day3 = {
            "name": start_date_month + '.' + info[2],
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        day4 = {
            "name": start_date_month + '.' + info[3],
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        day5 = {
            "name": start_date_month + '.' + info[4],
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        day6 = {
            "name": start_date_month + '.' + info[5],
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }
        day7 = {
            "name": start_date_month + '.' + info[6],
            "studyTime": 0,
            "restTime": 0,
            "otherTime": 0
        }

        cnt_month = int(day1["name"][:2])
        cnt_day = int(day1["name"][3:])
        for i in [day2, day3, day4, day5, day6, day7]:
            if int(i["name"][3:]) < cnt_day:
                i["name"] = str(cnt_month + 1) + '.' + i["name"][3:]
            if len(i["name"]) != 5:
                i["name"] = '0' + i["name"]

        for i in Actives:
            str_start_time = str(i.start_time)
            if str_start_time[:4] == start_date[:4] and str_start_time[5:7] == start_date[5:7]:
                if str_start_time[8:10] == info[0]:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            day1["studyTime"] += time
                        elif j.active_type == 0:
                            day1["restTime"] += time
                        else:
                            day1["otherTime"] += time
                elif str_start_time[8:10] == info[1]:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            day2["studyTime"] += time
                        elif j.active_type == 0:
                            day2["restTime"] += time
                        else:
                            day2["otherTime"] += time
                elif str_start_time[8:10] == info[2]:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            day3["studyTime"] += time
                        elif j.active_type == 0:
                            day3["restTime"] += time
                        else:
                            day3["otherTime"] += time
                elif str_start_time[8:10] == info[3]:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            day4["studyTime"] += time
                        elif j.active_type == 0:
                            day4["restTime"] += time
                        else:
                            day4["otherTime"] += time
                elif str_start_time[8:10] == info[4]:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            day5["studyTime"] += time
                        elif j.active_type == 0:
                            day5["restTime"] += time
                        else:
                            day5["otherTime"] += time
                elif str_start_time[8:10] == info[5]:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            day6["studyTime"] += time
                        elif j.active_type == 0:
                            day6["restTime"] += time
                        else:
                            day6["otherTime"] += time
                elif str_start_time[8:10] == info[6]:
                    for j in Active_Detail.filter(active=i.id):
                        time = calculateTime(j.startTime, j.endTime)
                        if j.active_type == 1:
                            day7["studyTime"] += time
                        elif j.active_type == 0:
                            day7["restTime"] += time
                        else:
                            day7["otherTime"] += time

        result.append(day1)
        result.append(day2)
        result.append(day3)
        result.append(day4)
        result.append(day5)
        result.append(day6)
        result.append(day7)

    elif search_type == 'day':
        for i in Actives:
            str_start_time = str(i.start_time)
            if str_start_time[:4] == start_date[:4] and str_start_time[5:7] == start_date[5:7] and str_start_time[8:10] == start_date[8:10]:
                for j in Active_Detail.filter(active=i.id):
                    data = {
                        "name": str(j.startTime)[11:16],
                        "studyTime": 0,
                        "restTime": 0,
                        "otherTime": 0
                    }
                    time = calculateTime(j.startTime, j.endTime)
                    if j.active_type == 1:
                        data["studyTime"] += time
                    elif j.active_type == 0:
                        data["restTime"] += time
                    else:
                        data["otherTime"] += time
                    result.append(data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_200_OK)