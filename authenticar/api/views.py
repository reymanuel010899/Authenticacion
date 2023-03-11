from datetime import datetime
from rest_framework.response import Response
from .serializers import User_serializer, UserRegistroView, serializer_update
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.views import APIView
from users.models import User
from .serializers import LoginZerializer




# Create your views here.

# aqui estoy logiando y creandole un token a el usuario 
class LoginView(APIView):

    '''This is the login view, in this view you can login and you can only open a section
      on a single computer, if it detects that they are trying to start a session on another computer,
        it automatically closes'''
    
    def post(self, request, *args, **kwargs):
        login_serializer = LoginZerializer(data=request.data)
        if login_serializer.is_valid():
            username = login_serializer.validated_data['username']
            usuario = User.objects.get(username=username)
            if usuario.is_active:
                user = User_serializer(usuario)
                token, created = Token.objects.get_or_create(user=usuario)
                if created:
                    return Response({'user':user.data, 'token':token.key}, status=status.HTTP_201_CREATED)
                else:
                    seciones = Session.objects.filter(expire_date__gte=datetime.now())
                    if seciones.exists():
                        for secion in seciones:
                            data = secion.get_decoded()
                            if usuario.id == int(data.get('_auth_user_id')):
                                secion.delete()
                    token.delete()
                    token = Token.objects.create(user=usuario)
                    return Response({'messege':'usuario creado exitoso', 'user':user.data,'token':token.key}, status=status.HTTP_200_OK)
            return Response({'error':'el usuario esta inactivo, intentelo en otro momento'}, status=status.HTTP_404_NOT_FOUND)    
        return Response({'usuario':'no encontrado , intente de nuevo'}, status=status.HTTP_404_NOT_FOUND)

  

# aqui estoy serrando la secion
class logoutView(APIView):

    '''This is the view to close the section, you just have to send me the user's token by parameters'''

    def get(self, request, *args, **kwargs):
        serializer =  User_serializer(data=request.data) 
        try:
            if serializer.is_valid():
                token_id = request.data.get('token_id')
                usuario = User.objects.get(auth_token__key=token_id)
                token = Token.objects.filter(key=token_id)
                if token.exists():
                    seciones = Session.objects.filter(expire_date__gte=datetime.now())
                    if seciones.exists():
                        for secion in seciones:
                            data = secion.get_decoded()
                            if usuario.id == int(data.get('_auth_user_id')):
                                secion.delete()
                    return Response({'messege':'secion serrada exitosa'})
                else:
                    return Response({'error':'no existen ningun usuario'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'introdusca el token'}, status=status.HTTP_400_BAD_REQUEST)
        except:
                return Response({'error':'hubo algun tipo de exepcion , intentelo de nuevo'}, status=status.HTTP_400_BAD_REQUEST)


#aqio estoy creando un usuario 
class  Crearusuarioview(APIView):

    '''In this view I create the user and encrypt the password'''
    serializer_class = UserRegistroView
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            gmail = serializer.validated_data['gmail']
            nombre = serializer.validated_data['nombre']
            apellido = serializer.validated_data['apellido']
            User.objects.create_user(username, gmail, password, nombre=nombre,apellido=apellido)
            return Response({'exito':'usuario creado sastifactoriamente'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'no introduciste los valores incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        
 



class  Userupdateview(APIView):
    serializer_class = serializer_update
    def post(self, request, *arg, **kwargs ):
        Userserializer = serializer_update(data=request.data) 
        if Userserializer.is_valid():
            try:
                username = self.request.data.get('username')
                user = User.objects.filter(username=username).first()   
                if user:
                    password = Userserializer.validated_data['password']
                    user.set_password(password)
                    return Response({'password':'password cambiado correctamente'})
                else:
                    return Response({'user':'invalido'}, status=status.HTTP_404_NOT_FOUND)
                   
            except:
                 return Response({"messege":'introduzca ls datos bien'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"messege":'introduzca los datos bien'}, status=status.HTTP_404_NOT_FOUND)


