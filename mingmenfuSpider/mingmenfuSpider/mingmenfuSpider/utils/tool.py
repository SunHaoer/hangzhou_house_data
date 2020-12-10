
def get_community_name(community_str):
    result = '-'
    if '名门府' in community_str or '汇雅轩' in community_str:
        result = '名门府'
    elif '春江悦茗' in community_str:
        result = '春江悦茗'
    elif '华瑞晴庐' in community_str:
        result = '华瑞晴庐'
    elif '银爵' in community_str:
        result = '银爵世纪'
    elif '莱蒙水榭山' in community_str or '微风之城' in community_str:
        result = '微风之城'
    elif '望海潮' in community_str:
        result = '望海潮'
    elif '璟隽' in community_str:
        result = '璟隽公馆'
    return result
