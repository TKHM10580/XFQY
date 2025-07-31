import streamlit as st
import pandas as pd
import sys
import os
import time

# 添加标题
st.title("个人xlsx处理工具")

# 添加侧边栏
with st.sidebar:
    company_key = st.text_input("输入公司密码",type="password")
    button_1 = st.button("1. 打印历史内容")
    button_2 = st.button("2. 打印网段内容")
    button_3 = st.button("3. 添加网段内容")
    button_4 = st.button("4. 删除网段内容")
    button_5 = st.button("5. 执行文件")

定义 rsa密钥(密钥):
    如果 键 是 无:
        返回 "请输入公司密码"
    elif key != 'aopnt.com':
        返回 “公司密码错误”
    否则:
        返回 真

结果 = rsa_key(公司密钥)
如果 结果 是 真:
    通过
否则:
    st.信息(结果)
    街。停止()


data = st.file_uploader("上传你的数据文件（excel格式）：", type=["xlsx", "xls", "csv"])

if data:
    st.session_state["df"] = pd.read_excel(data)
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])



def get_resource_path(relative_path):
    """ 动态获取资源路径，兼容开发与打包环境 """
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# 定义网段解析网址函数
def base_ip(masklist):
    mask_list = masklist
    ip_list = []
    for baseip in mask_list:
       str_mask = baseip.split("/")[-1]
       int_mask = int(str_mask)
       mun_client = 2**(32 - int_mask) - 2
       client = baseip.split("/")[0].split(".")[-1]
       int_client = int(client)
       str_network = ".".join(baseip.split('.')[:3])
       list_baseip = [str_network + "." + str(i) for i in range(int_client+1, int_client+1+mun_client)]
       ip_list=ip_list+list_baseip
    return ip_list

# 定义查询网址函数
def ip_check(ip):
    try:
        # ip_tab = str(desktop_path) + "\\" + "network.xlsx"
        ip_tab = get_resource_path('network.xlsx')
        df5 = pd.read_excel(ip_tab)
        client_list = df5["客户"].value_counts().index.tolist()
        for client in client_list:
            client_info = df5.query(f'(客户 == "{client}")')
            client_mask = client_info["业务网段"].tolist()
            client_owner = client_info["对接名称"].value_counts().index.tolist()[0]
            # print(f"{client}所拥有的网段为{client_mask}")
            client_ip = base_ip(client_mask)
            # print(f"{client}的网址IP为{client_ip}")
            if ip in client_ip:
               return client,client_owner
        return None
    except ValueError:
        return "Error"

# st.session_state.df3 = pd.read_excel(get_resource_path('history.xlsx'))
# st.session_state.net_df = pd.read_excel(get_resource_path('network.xlsx'))

if "history" not in st.session_state:
    st.session_state["history"] = None
if "network" not in st.session_state:
    st.session_state["network"] = None
if "show_form" not in st.session_state:
    st.session_state["show_form"] = False
if "del_form" not in st.session_state:
    st.session_state["del_form"] = False
if "clear_data" not in st.session_state:
    st.session_state["clear_data"] = None
if "txt_list" not in st.session_state:
    st.session_state["txt_list"] = []


if button_1:
    st.session_state["history"]  =  pd.read_excel(get_resource_path('history.xlsx'))

if button_2:
    st.session_state["network"] = pd.read_excel(get_resource_path('network.xlsx'))

if button_3 and not st.session_state["show_form"]:
    st.session_state["show_form"] = True

if st.session_state["show_form"]:
    with st.form("add_network_form"):
        client = st.text_input("客户名称*", placeholder="必填")
        url = st.text_input("业务网段*", placeholder="格式: 192.168.1.0/24")
        company_type = st.text_input("对接名称*", placeholder="必填")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("提交")
        with col2:
            cancel = st.form_submit_button("取消")

        if submitted:
            if not (client and url and company_type):  # 必填验证
                st.warning("带*字段为必填项")
            else:
                new_row = {"客户": client, "业务网段": url, "对接名称": company_type}
                st.session_state["network"] = pd.read_excel(get_resource_path('network.xlsx'))
                st.session_state["network"] = pd.concat([st.session_state["network"], pd.DataFrame(new_row, index=[0])], ignore_index=True)
                st.session_state["network"].to_excel(get_resource_path('network.xlsx'), index=False)
                st.write("数据添加成功")
                st.session_state.show_form = False
                time.sleep(1)
                st.rerun()
        if cancel:
            st.session_state.show_form = False
            st.rerun()
if button_4 and not st.session_state["del_form"]:
    st.session_state["del_form"] = True

if st.session_state["del_form"]:
    with st.form("del_network_form"):
        st.session_state["network"] = pd.read_excel(get_resource_path('network.xlsx'))
        del_data = st.number_input("请输入要删除的行：", value=0, min_value=0,
                                   max_value=len(st.session_state["network"])-1, step=1)
        col3, col4 = st.columns(2)
        with col3:
            submitted_2 = st.form_submit_button("提交")
        with col4:
            cancel_2 = st.form_submit_button("取消")
        if submitted_2:
            if len(st.session_state["network"]) == 0:
                st.warning("没有数据可删除！")
                st.session_state.del_form = False
            else:
                st.session_state["network"] = st.session_state["network"].drop(int(del_data)).reset_index(drop=True)
                st.session_state["network"].to_excel(get_resource_path('network.xlsx'), index=False)
                st.success("删除成功")
                st.session_state.del_form = False
                time.sleep(1)
                st.rerun()
        if cancel_2:
            st.session_state.del_form = False
            st.rerun()

if button_5:
    st.session_state["history"] = pd.read_excel(get_resource_path('history.xlsx'))
    st.session_state["network"] = pd.read_excel(get_resource_path('network.xlsx'))
    df2 = st.session_state["df"].copy()
    df2 = df2.drop_duplicates(subset=['域名', '访问地址'])
    df2 = df2.dropna(subset=["域名"])
    df2.reset_index(drop=True, inplace=True)
    df2['序号'] = range(1, len(df2) + 1)
    st.session_state["clear_data"] = df2
    for x in df2["域名"].tolist():
        if x in st.session_state["history"]["域名"].tolist():
            st.session_state["txt_list"].append(f"域名{x}存在重复")
        elif x not in st.session_state["history"]["域名"].tolist():
            index = df2["域名"][df2["域名"] == x].index[0]
            st.session_state["history"].loc[len(st.session_state["history"])] = df2.iloc[index]
            st.session_state["txt_list"].append(f"域名{x}不存在重复，已加入历史")

    sorted_history = st.session_state["history"].sort_values(by='存活检测时间', ascending=True)
    sorted_history.reset_index(drop=True, inplace=True)
    sorted_history['序号'] = range(1, len(sorted_history) + 1)
    sorted_history.to_excel(get_resource_path('history.xlsx'), index=False)

    for index, row in df2[["解析IP", "域名"]].iterrows():
        result = ip_check(row["解析IP"])
        if result == "Error":
            st.warning("未知错误，检查文件或ip")
            time.sleep(1)
            st.stop()
        elif result is not None:
            client, owner = result
            ip = f'域名{row["域名"]}，地址{row["解析IP"]}业务在{client},使用{owner}回复邮件'
            st.session_state["txt_list"].append(ip)
        else:
            ip = f'域名{row["域名"]}，地址{row["解析IP"]}业务在地址未知位置地址段'
            st.session_state["txt_list"].append(ip)


如果 st.session_state["历史记录"] 不是 无 None:
    与 st.扩展器("以往历史"):
        st.dataframe(st.session_state["history"])

如果 st.session_state["network"] 不是  None :
    与 st.扩展器("业务网段"):
        st.dataframe(st.session_state["network"])

如果 st.session_state["clear_data"] 不是 None :
    与 st.扩展器("清洗文件"):
        st.dataframe(st.session_state["clear_data"])

如果 st.session_state["txt_list"] 不是 None :
    与 st.扩展器("执行结果"):
        st.writest.session_state["txt_list"].strip()write(session_state["txt_list"].strip())
