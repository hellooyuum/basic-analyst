import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_most_sell_sellers_df(df):
  most_sell_sellers_df = df.groupby(by="seller_id").agg({
    "order_item_id": "sum",
    "payment_value": "sum",
  }).sort_values(by="payment_value", ascending=False).reset_index()

  return most_sell_sellers_df

def create_sum_order_items_df(df):
  sum_order_items_df = df.groupby("product_category_name").order_item_id.sum().sort_values(ascending=False).reset_index()

  return sum_order_items_df

def create_monthly_orders_df(df):
  monthly_orders_df = df.resample(rule='M', on='order_approved_at').agg({
      "order_id": "nunique",
      "payment_value": "sum"
  })
  monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
  monthly_orders_df = monthly_orders_df.reset_index()
  monthly_orders_df.rename(columns={
      "order_id": "order_count",
      "payment_value": "revenue"
  }, inplace=True)

  return monthly_orders_df

def create_product_review_df(df):
  product_review_df = df.groupby("product_category_name").review_score.sum().sort_values(ascending=True).reset_index()

  return product_review_df

def create_customer_bystate_df(df):
  customer_bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
  customer_bystate_df.rename(columns={
      "customer_id": "customer_count"
  }, inplace=True)

  return customer_bystate_df

def create_seller_bystates_df(df):
  seller_bystates_df = df.groupby(by="seller_state").seller_id.nunique().sort_values(ascending=False).reset_index()
  seller_bystates_df.rename(columns={
      "seller_id": "seller_count"
  }, inplace=True)

  return seller_bystates_df

all_df = pd.read_csv("all_datafix.csv")

datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

    min_date = all_df["order_approved_at"].min()
    max_date = all_df["order_approved_at"].max()

with st.sidebar: start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                (all_df["order_approved_at"] <= str(end_date))]

most_sell_sellers_df = create_most_sell_sellers_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
monthly_orders_df = create_monthly_orders_df(main_df)
product_review_df = create_product_review_df(main_df)
customer_bystate_df = create_customer_bystate_df(main_df)
seller_bystates_df = create_seller_bystates_df(main_df)

st.header('E-Commerce Public Dashboard :sparkles:')

st.subheader('Most Sell and Revenue by Sellers')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(50, 15))

colors = ["#331CFF", "#5349FD", "#7377FB", "#93A4F9", "#B3D1F7"]

sns.barplot(
     x="seller_id", 
     y="order_item_id", 
     data=most_sell_sellers_df.sort_values(by="order_item_id", ascending=False).head(5), 
     palette=colors, ax=ax[0]
    )
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Most Sales by Sellers", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=35)
ax[0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

legend_labels_1 = ['1f50f920176fa81dab994f9023523100', '4a3ca9315b744ce9f8e9374361493884', '6560211a19b47992c3666cc44a7e94c0', '1025f0e2d44d7041d6cf58b6550e0bfa', '7c67e1448b00f6e969d365cea6b010ab']
legend_handles_1 = [plt.Line2D([0], [0], color=color, lw=4, label=label) for color, label in zip(colors, legend_labels_1)]
ax[0].legend(handles=legend_handles_1, loc='upper center', bbox_to_anchor=(0.5, -0.0), ncol=1, prop={'size': 50})

sns.barplot(
     x="seller_id", 
     y="payment_value", 
     data=most_sell_sellers_df.sort_values(by="payment_value", ascending=False).head(5), 
     palette=colors, 
     ax=ax[1]
    )
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Most Revenue by Sellers", loc="center", fontsize=50)
ax[1].tick_params(axis ='y', labelsize=35)
ax[1].tick_params(axis ='x', labelsize=35)
ax[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

legend_labels_2 = ['7c67e1448b00f6e969d365cea6b010ab', '1025f0e2d44d7041d6cf58b6550e0bfa', '4a3ca9315b744ce9f8e9374361493884', '1f50f920176fa81dab994f9023523100', '53243585a1d6dc2643021fd1853d8905']
legend_handles_2 = [plt.Line2D([0], [0], color=color, lw=4, label=label) for color, label in zip(colors, legend_labels_2)]
ax[1].legend(handles=legend_handles_2, loc='upper center', bbox_to_anchor=(0.5, -0.0), ncol=1, prop={'size': 50})
st.pyplot(fig)

st.subheader('Most Sell by Product')

fig, ax = plt.subplots(figsize=(60, 30))

colors_ = ["#331CFF", "#4333FE", "#5349FD", "#6360FC", "#7377FB", "#838DFA", "#93A4F9", "#A3BBF8", "#B3D1F7", "#C3E8F6"]
sns.barplot(
    x="product_category_name",
    y="order_item_id",
    data=sum_order_items_df.sort_values(by="order_item_id", ascending=False).head(10),
    palette=colors_
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=40)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
legend_most_sell = ['cama_mesa_banho', 'moveis_decoracao', 'beleza_saude', 'esporte_lazer', 'informatica_acessorios', 'utilidades_domesticas', 'relogios_presentes', 'ferramentas_jardim', 'telefonia', 'automotivo']
legend_colors = colors_[:len(legend_most_sell)]
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors]
plt.legend(handles=legend_handles, labels=legend_most_sell, loc='upper center', bbox_to_anchor=(0.2, 0.0), ncol=2, prop={'size': 50})
st.pyplot(fig)

st.subheader('Worst Sell by Product')

fig, ax = plt.subplots(figsize=(60, 30))

colors_ = ["#331CFF", "#4333FE", "#5349FD", "#6360FC", "#7377FB", "#838DFA", "#93A4F9", "#A3BBF8", "#B3D1F7", "#C3E8F6"]
sns.barplot(
    x="product_category_name",
    y="order_item_id",
    data=sum_order_items_df.sort_values(by="order_item_id", ascending=True).head(10),
    palette=colors_
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.invert_xaxis()
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=40)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
legend_worst_sell = ['seguros_e_servicos', 'fashion_roupa_infanto_juvenil', 'pc_gamer', 'portateis_cozinha_e_preparadores_de_alimentos', 'cds_dvds_musicais', 'la_cuisine', 'artes_e_artesanato', 'flores', 'fashion_esporte', 'casa_conforto_2']
legend_colors = colors_[:len(legend_most_sell)]
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors]
plt.legend(handles=legend_handles, labels=legend_worst_sell, loc='upper center', bbox_to_anchor=(0.3, 0.0), ncol=2, prop={'size': 50})
st.pyplot(fig)

st.subheader('Orders per Month')

total_orders = monthly_orders_df.order_count.sum()
st.metric("Total orders", value=total_orders)

fig, ax = plt.subplots(figsize=(35, 15))

ax.plot(
  monthly_orders_df["order_approved_at"], 
  monthly_orders_df["order_count"], 
  marker='o', 
  linewidth=2, 
  color="#331CFF"
  )
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='x', rotation=60)
st.pyplot(fig)

st.subheader('Revenue per Month')

total_revenue = format_currency(monthly_orders_df.revenue.sum(), "AUD", locale='es_CO') 
st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(35, 15))

ax.plot(
    monthly_orders_df["order_approved_at"],
    monthly_orders_df["revenue"],
    marker='o',
    linewidth=2,
    color="#331CFF"
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='x', rotation=60)
st.pyplot(fig)

st.subheader('Best and Worst Product by Review Score')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#331CFF", "#5349FD", "#7377FB", "#93A4F9", "#B3D1F7"]

sns.barplot(
  x="product_category_name", 
  y="review_score", 
  data=product_review_df.head(5), 
  palette=colors, ax=ax[0]
  )
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Review Score Product", loc="center", fontsize=10)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(
  x="product_category_name", 
  y="review_score", 
  data=product_review_df.sort_values(by="review_score", ascending=True).head(5), 
  palette=colors, ax=ax[1]
  )
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Review Score Product", loc="center", fontsize=15)
ax[1].tick_params(axis ='y', labelsize=12)
ax[1].tick_params(axis='x', labelsize=5)
st.pyplot(fig)

st.subheader('Number of Customers by States')

fig, ax = plt.subplots(figsize=(20, 10))
colors_ = ["#331CFF", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6"]
sns.barplot(
    x="customer_count",
    y="customer_state",
    data=customer_bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors_
)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=8)
st.pyplot(fig)

st.subheader('Number of Sellers by States')

fig, ax = plt.subplots(figsize=(20, 10))
colors_ = ["#331CFF", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6", "#C3E8F6"]
sns.barplot(
    x="seller_count",
    y="seller_state",
    data=seller_bystates_df.sort_values(by="seller_count", ascending=False),
    palette=colors_
)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=8)
st.pyplot(fig)

st.markdown("### Detailed Data View")
st.dataframe(all_df)