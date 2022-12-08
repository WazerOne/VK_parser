import csv
import requests
import time
import pandas as pd

def get_wallposts(user_id, n):
    token = "f3b0a247f3b0a247f3b0a24714f0a16bdaff3b0f3b0a24790200193ca9a669a8f2fb921"
    version = 5.131
    filter = 'all'
    extended = 1
    fields = 'groups'
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v': version,
                                'owner_id': user_id,
                                'count': n,
                                'filter': filter,
                                'extended': extended,
                                'fields': fields
                            }
                            )
    dataW = response.json()['response']['items']
    return dataW


def get_subscribtions(user_id, n):
    token = "f3b0a247f3b0a247f3b0a24714f0a16bdaff3b0f3b0a24790200193ca9a669a8f2fb921"
    version = 5.131
    extended = 1
    offset = 0
    fields = 'groups'
    response = requests.get('https://api.vk.com/method/users.getSubscriptions',
                            params={
                                'access_token': token,
                                'v': version,
                                'user_id': user_id,
                                'extended': extended,
                                'offset': offset,
                                'count': n,
                                'fields': fields
                            }
                            )
    dataW = response.json()['response']['items']
    return dataW



# def parser_vk(links):
#     with open('VK_parser_posts', 'w', encoding='utf-8') as file_posts:
#         with open('VK_parser_subs', 'w', encoding='utf-8') as file_subs:
#             a_pen = csv.writer(file_posts)
#             a_pen.writerow((('user_id', 'id_post', 'text')))
#             b_pen = csv.writer(file_subs)
#             b_pen.writerow((('user_id', 'group_id', 'group_name')))
#             for link in links:
#                 time.sleep(0.5)
#                 user_id = link.partition('id')[2]
#                 TWpost = get_wallposts(user_id, 20)
#                 TWsubs = get_subscribtions(user_id, 200)
#                 for post in TWpost:
#                     if post['text'] != '':
#                         a_pen.writerow((user_id, post['id'], post['text']))
#                 for sub in TWsubs:
#                     if sub['type'] != 'profile':
#                         b_pen.writerow((user_id, sub['id'], sub['name']))

def parser_vk(links):
    df_posts = pd.DataFrame({'user_id': [],
                             'post_id': [],
                             'post_text': []})

    df_subs = pd.DataFrame({'user_id': [],
                            'group_id': [],
                            'group_name': []})
    for link in links:
        user_id = link.partition('id')[2]
        TWposts = get_wallposts(user_id, 20)
        for post in TWposts:
            if post['text'] != '':
                df_posts.loc[len(df_posts.index)] = [user_id, post['id'], post['text']]
        TWsubs = get_subscribtions(user_id, 200)
        for sub in TWsubs:
            if sub['type'] != 'profile':
                df_subs.loc[len(df_subs.index)] = [user_id, sub['id'], sub['name']]
        time.sleep(0.5)
    return df_posts, df_subs


links = ['http://vk.com/id101835572', 'http://vk.com/id102840485']

posts, subs = parser_vk(links)

with pd.ExcelWriter('C:/Users/wazer/PycharmProjects/vkparser/VK_parser.xlsx') as writer:
    posts.to_excel(writer, sheet_name='Posts')
    subs.to_excel(writer, sheet_name='Subs')

print(1)

# def write_txt_post_to_csv(TWpost):
#     with open('Lazitch_posts', 'w', encoding='utf-8') as file:
#         a_pen = csv.writer(file)
#         a_pen.writerow(('id_post', 'text'))
#         for i in TWpost:
#             a_pen.writerow((i['id'], i['text']))
#
#
# def write_txt_subs_to_csv(TWsubs):
#     with open('Lazitch_subs', 'w', encoding='utf-8') as file:
#         a_pen = csv.writer(file)
#         a_pen.writerow(('id', 'name'))
#         for i in TWsubs:
#             a_pen.writerow((i['id'], i['name']))
#
#
#
#
# TWsubs = get_subscribtions(200)
# write_txt_subs_to_csv(TWsubs)
#
# TWpost = get_wallposts(20)
# write_txt_post_to_csv(TWpost)
#
# def parser_vk(links):
#     with open('VK_parser_posts', 'w', encoding='utf-8') as file_posts:
#         with open('VK_parser_subs', 'w', encoding='utf-8') as file_subs:
#             a_pen = csv.writer(file_posts)
#             a_pen.writerow((('user_id', 'id_post', 'text')))
#             b_pen = csv.writer(file_subs)
#             b_pen.writerow((('user_id', 'group_id', 'group_name')))
#             for link in links:
#                 time.sleep(0.5)
#                 user_id = link.partition('id')[2]
#                 TWpost = get_wallposts(user_id, 20)
#                 TWsubs = get_subscribtions(user_id, 200)
#                 for post in TWpost:
#                     if post['text'] != '':
#                         a_pen.writerow((user_id, post['id'], post['text']))
#                 for sub in TWsubs:
#                     if sub['type'] != 'profile':
#                         b_pen.writerow((user_id, sub['id'], sub['name']))
