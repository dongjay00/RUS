from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer
from .models import User, Group

import boto3
from datetime import datetime
import environ

env = environ.Env(
    DEBUG=(bool,True)
)
environ.Env.read_env()

# Create your views here.
# 회원 상세 정보
@api_view(['GET'])
def get_user_info(request, user_pk):
    Users = User.objects.all()
    user_info = get_object_or_404(Users, pk=user_pk)
    serializer = UserSerializer(user_info)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

# 신규 회원 여부
@api_view(['GET'])
def is_user_in_db(request, account_email):
    if User.objects.filter(account_email=account_email).exists():
        user_info = User.objects.get(account_email=account_email)
        user_pk = user_info.id
        return Response({'message': '이미 등록된 유저입니다.', 'user_pk': user_pk}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'message': '없는 회원입니다.', 'user_pk': 'null'}, status=status.HTTP_202_ACCEPTED)

# DB에 신규 회원 정보 저장
@api_view(['POST'])
def save_user_to_db(request):
    if request.data["profile_img"] == "":
        request.data["profile_img"] = "https://rus-image.s3.ap-northeast-2.amazonaws.com/2021-04-0214:26:19.002423.jpeg"
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        Users = User.objects.all()
        user_info = get_object_or_404(Users, pk=serializer.data["id"])
        Groups = Group.objects.all()
        group_info = get_object_or_404(Groups, pk=25)
        group_info.member.add(user_info)
    return Response({'user_pk': serializer.data["id"]}, status=status.HTTP_201_CREATED)

# 가입한 그룹 목록
@api_view(['GET'])
def get_my_groups(request, user_pk):
    Users = User.objects.all()
    my_info = get_object_or_404(Users, pk=user_pk)
    my_groups = my_info.group.all()
    serializer = GroupSerializer(my_groups, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
# 전체 그룹 목록
@api_view(['GET'])
def get_all_groups(request, user_pk):
    group_infos = []
    Groups = Group.objects.all()
    for i in Groups:
        group_info = {
            "id": i.id,
            "name": i.name,
            "leader_pk": i.leader_pk,
            "max_user": i.max_user,
            "group_img": i.group_img,
            "description": i.description,
            "member": [],
            "participate": "false"
        }
        for j in i.member.all():
            member_pk = j.id
            group_info["member"].append(member_pk)
        if user_pk in group_info["member"]:
            group_info["participate"] = "true"
        group_infos.append(group_info)
    return Response(group_infos, status=status.HTTP_202_ACCEPTED)

# 그룹 상세 정보, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def get_update_delete_group_info(request, group_pk):
    Groups = Group.objects.all()
    group_info = get_object_or_404(Groups, pk=group_pk)
    if request.method == 'GET':
        group_serializer = GroupSerializer(group_info)
        leader = User.objects.get(pk=group_info.leader_pk)
        leader_serializer = UserSerializer(leader)
        group_members = group_info.member.all()
        member_serializer = UserSerializer(group_members, many=True)
        return Response({"group_info": group_serializer.data, "leader_info": leader_serializer.data, "members_info": member_serializer.data}, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'PUT':
        data = request.data
        
        group_info.name = data["name"]
        group_info.leader_pk = data["leader_pk"]
        group_info.max_user = data["max_user"]
        group_info.group_img = data["group_img"]
        group_info.description = data["description"]
        group_info.name = data["name"]
        
        group_info.save()

        group_serializer = GroupSerializer(group_info)

        leader = User.objects.get(pk=data["leader_pk"])
        leader_serializer = UserSerializer(leader)

        group_members = group_info.member.all()
        member_serializer = UserSerializer(group_members, many=True)

        return Response({"group_info": group_serializer.data, "leader_info": leader_serializer.data, "members_info": member_serializer.data}, status=status.HTTP_202_ACCEPTED)
    else:
        group_info.delete()
        return Response({"group_pk": group_pk}, status=status.HTTP_204_NO_CONTENT)

# 그룹 참여 회원 정보 목록
@api_view(['GET'])
def get_group_members(request, group_pk):
    Groups = Group.objects.all()
    group_info = get_object_or_404(Groups, pk=group_pk)
    group_members = group_info.member.all()
    serializer = UserSerializer(group_members, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

# 그룹 참여 회원 수
@api_view(['GET'])
def get_group_member_count(request, group_pk):
    Groups = Group.objects.all()
    group_info = get_object_or_404(Groups, pk=group_pk)
    group_members = group_info.member.all()
    serializer = UserSerializer(group_members, many=True)
    return Response({"member_count": len(serializer.data)}, status=status.HTTP_202_ACCEPTED)

# 그룹 생성
@api_view(['POST'])
def create_group(request, user_pk):
    user_info = User.objects.get(pk=user_pk)
    data = request.data
    new_group = Group.objects.create(
        name=data["name"],
        leader_pk=data["leader_pk"],
        max_user=data["max_user"],
        group_img=data["group_img"],
        description=data["description"]
    )
    new_group.save()
    new_group.member.add(user_info)
    serializer = GroupSerializer(new_group)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# 그룹 이미지 업로드
@api_view(['POST'])
def upload_group_image(request):
    # image
    s3_client = boto3.client(
        's3',
        aws_access_key_id = env("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = env("AWS_SECRET_ACCESS_KEY")
    )

    image = request.FILES['filename']  # formdata 키 : filename으로 이미지를 받는다.
    image_time = (str(datetime.now())).replace(" ","") # 이미지이름을 시간으로 설정하기 위해 datetime를 사용했다.
    image_type = (image.content_type).split("/")[1]
    s3_client.upload_fileobj(
        image,
        "rus-image", # 버킷이름
        image_time+"."+image_type,
        ExtraArgs = {
            "ContentType" : image.content_type
        }
    )
    aws_url = env("AWS_URL")
    image_url = str(aws_url)+image_time+"."+image_type  # 업로드된 이미지의 url이 설정값으로 저장됨
    image_url = image_url.replace(" ","/")

    return Response({"image_url": image_url}, status=status.HTTP_201_CREATED)

# 그룹 참여, 탈퇴
@api_view(['PUT', 'DELETE'])
def participate_leave_group(request, user_pk, group_pk):
    Users = User.objects.all()
    user_info = get_object_or_404(Users, pk=user_pk)
    Groups = Group.objects.all()
    group_info = get_object_or_404(Groups, pk=group_pk)
    if request.method == 'PUT':
        group_info.member.add(user_info)
    else:
        group_info.member.remove(user_info)
    serializer = GroupSerializer(group_info)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)