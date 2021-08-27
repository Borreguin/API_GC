# Statements that will be executed for the different views:
# Views:
info_personal_basica = 'SELECT * FROM [GESTION_CONOCIMIENTO].[dbo].[INFORMACION_PERSONAL_BASICA]'
contactos_emergencia = 'SELECT * FROM [GESTION_CONOCIMIENTO].[dbo].[CONTACTOS_EMERGENCIA]'
capacitacion_sith = 'SELECT * FROM [GESTION_CONOCIMIENTO].[dbo].[CAPACITACION_SITH]'
funcionarios_inicio_cargo = 'SELECT * FROM [GESTION_CONOCIMIENTO].[dbo].[FUNCIONARIOS_INICIO_CARGO]'
funcionarios_direccion = 'SELECT * FROM [GESTION_CONOCIMIENTO].[dbo].[INFORMACION_PERSONAL_DIRECCION]'
funcionarios_info_basica = 'SELECT * FROM [GESTION_CONOCIMIENTO].[dbo].[FUNCIONARIOS_INFO_BASICA]'
persona_table = 'SELECT * FROM [GESTION_CONOCIMIENTO].[dbo].[PERSONA]'

# Special Statements:
asp_net_user_basic_info = 'SELECT [Id],[UserName],[NormalizedUserName],[Email],[PhoneNumber] ' \
                          'FROM [APPSecurityGC].[dbo].[AspNetUsers]'