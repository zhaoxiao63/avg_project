import re


def camel_to_snake(name):
    # 使用正则表达式将驼峰命名转换为下划线命名
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    # 将所有大写字母转换为小写字母
    return s1.lower()


if __name__ == '__main__':
    camel_case_name = "aAbBcCdD"
    snake_case_name = camel_to_snake(camel_case_name)
    print(snake_case_name)  # 输出：camel_case_example
