from datetime import datetime

def format_time_ago(created_time):
    """
    将datetime对象转换为'xx时间前'的格式
    如果超过24小时则返回具体的创建时间
    
    参数:
    created_time: datetime对象
    
    返回:
    str: 格式化后的时间字符串
    """
    if not isinstance(created_time, datetime):
        return str(created_time)
    
    now = datetime.now()
    diff = now - created_time
    
    # 如果超过24小时，直接返回具体时间
    if diff.days > 0:
        return created_time.strftime('%Y-%m-%d %H:%M')
    
    # 如果是几小时前
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours}小时前"
    
    # 如果是几分钟前
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes}分钟前"
    
    # 如果是几秒前
    else:
        return "刚刚"


