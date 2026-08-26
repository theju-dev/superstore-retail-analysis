import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("data/Sample - Superstore.csv",encoding="latin1")
print(df.head())
print("\nDATASET SHAPE")
print(df.shape)
print("\nCOLUMN NAMES")
print(df.columns)
print("\nDATASET INFO")
df.info()
print("\nMISSING VALUES")
print(df.isnull().sum())
print("\nDUPLICATE ROWS")
print(df.duplicated().sum())
print("\n TOTAL ROWS")
print(len(df))
print("\nUNIQUE ORDERS")
print(df["Order ID"].nunique())
print("\nUNIQUE CUSTOMERS")
print(df["Customer ID"].nunique())
print("\n DATA TYPES")
print(df.dtypes)
df["Order Date"]=pd.to_datetime(df["Order Date"])
df["Ship Date"]=pd.to_datetime(df["Ship Date"])
print("\n After the conversion:",df[["Order Date","Ship Date"]].dtypes)
df["Order year"]=df["Order Date"].dt.year
df["Order Month"]=df["Order Date"].dt.month
df["Year-Month"]=df["Order Date"].dt.to_period("M")
df["Shipping Days"]=(df["Ship Date"]-df["Order Date"]).dt.days
print("\n DATE CHECK")
print(df[["Order Date","Ship Date","Order year","Order Month","Year-Month","Shipping Days"]].head())
total_sales=df["Sales"].sum()
total_profit=df["Profit"].sum()
total_orders=df["Order ID"].nunique()
total_customers=df["Customer ID"].nunique()
print("Total Sales:",total_sales)
print("Total Profit:",total_profit)
print("Total orders:",total_orders)
print("Total customers:",total_customers)
category_profit=df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
print("\nProfit by category")
print(category_profit)
subcategory_profit=df.groupby("Sub-Category")["Profit"].sum().sort_values(ascending=True)
print(subcategory_profit)
bottom_5_subcategories=df.groupby("Sub-Category")["Profit"].sum().sort_values(ascending=True).head(5)
print(bottom_5_subcategories)
bottom_5_subcategories.plot(kind="bar")
plt.title("Bottom 5 subcategories by profit")
plt.xlabel("Sub-Category")
plt.ylabel("Total profit")
plt.tight_layout()
plt.savefig("charts/Sub-Category_botton5.png")
plt.show()
category_analysis=df.groupby("Category").agg(total_sales=("Sales","sum"),
                                             total_profit=("Profit","sum"),
                                             avg_discount=("Discount","mean"),
                                             order_lines=("Order ID","nunique")).reset_index().sort_values("total_profit",ascending=False)
print(category_analysis)
subcategory_analysis=df.groupby("Sub-Category").agg(total_sales=("Sales","sum"),
                                             total_profit=("Profit","sum"),
                                             avg_discount=("Discount","mean"),
                                             order_lines=("Order ID","nunique")).reset_index().sort_values("total_profit")
loss_orders=df[df["Profit"]<0]
print("\nNUMBER OF LOSS MAKING ROWS")
print(len(loss_orders))
print(type(loss_orders))
loss_by_subcategory=loss_orders.groupby("Sub-Category")["Profit"].sum().sort_values(ascending=True)
print("\n LOSSES BY SUB-CATEGORY")
print(loss_by_subcategory)
avg_discount_loss=loss_orders["Discount"].mean()
print(avg_discount_loss)
profitable_orders=df[df["Profit"]>0]
avg_discount_profit=profitable_orders["Discount"].mean()
print(avg_discount_profit)
discount_analysis=df.groupby("Discount").agg(total_sales=("Sales","sum"),
                           total_profit=("Profit","sum"),
                           order_lines=("Order ID","count")).reset_index()
print("\n DISCOUNT ANALYSIS")
discount_analysis["Discount %"]=discount_analysis["Discount"]*100
print(discount_analysis)
plt.bar(discount_analysis["Discount %"],discount_analysis["total_profit"])
plt.title("Profit by discount level")
plt.xlabel("Discount [%]")
plt.ylabel("Total Profit")
plt.tight_layout()
plt.savefig("charts/discount_analysis.png")
plt.show()
subcategory_discount_analysis=df.groupby("Sub-Category").agg(avg_discount=("Discount","mean"),
                                                             total_profit=("Profit","sum"),
                                                             total_sales=("Sales","sum"))
print("\n Sub-category discount analysis")
print(subcategory_discount_analysis)
furniture_df=df[df["Category"]=="Furniture"]
furniture_analysis=furniture_df.groupby("Sub-Category").agg(total_sales=("Sales","sum"),
                                         total_profit=("Profit","sum"),
                                         avg_discount=("Discount","mean")).sort_values("total_profit")
#region_profit=df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
print("\n Furniture Analysis")
print(furniture_analysis)
region_profit=df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
print("\nProfit by region")
print(region_profit)
state_profit=df.groupby("State")["Profit"].sum().sort_values()
print("\n Bottom 10 states by profit")
print(state_profit)
#print(state_profit.head(10))
state_analysis=df.groupby("State").agg(total_sales=("Sales","sum"),
                        total_profit=("Profit","sum"),
                        avg_discount=("Discount","mean"),
                        order_lines=("Order ID","count"),
                        unique_orders=("Order ID","nunique")).reset_index().sort_values("total_profit")
print("\n state analysis")
state_analysis["avg_discount_pct"]=state_analysis["avg_discount"]*100
print(state_analysis)
state_subcategory_analysis=df.groupby(["State","Sub-Category"]).agg(total_sales=("Sales","sum"),
                                                                    total_profit=("Profit","sum"),
                                                                    avg_discount=("Discount","mean")).sort_values("total_profit")
state_subcategory_analysis["avg_discount_pct"]=state_subcategory_analysis["avg_discount"]*100
print(state_subcategory_analysis.head(10))
product_loss_analysis=df.groupby(["State","Sub-Category","Product Name"]).agg(total_sales=("Sales","sum"),
                                                                              total_profit=("Profit","sum"),
                                                                              avg_discount=("Discount","mean"),
                                                                              unique_orders=("Order ID","nunique")).reset_index().sort_values(by="total_profit")
print("\n WORST PRODUCT LEVEL LOSSES")
print(product_loss_analysis.head(10))
worst_product_transactions=df[(df["State"]=="Ohio") & (df["Product Name"].str.contains("Cubify cubex",case=False,na=False)) & (df["Sub-Category"]=="Machines")]
print(worst_product_transactions[["Order ID","Order Date","Product Name","Sales","Quantity","Discount","Profit"]])
df["Discount Band"]=pd.cut(df["Discount"],bins=[-0.01,0,0.2,0.4,0.6,0.8],labels=["0%","1-20%","21-40%","41-60%","61-80%"])
print(df)
discount_band_analysis=df.groupby("Discount Band").agg(total_sales=("Sales","sum"),
                                total_profit=("Profit","sum"),
                                order_lines=("Order ID","count")).reset_index()
print(discount_band_analysis)
segment_analysis=df.groupby("Segment").agg(total_sales=("Sales","sum"),
                                           total_profit=("Profit","sum"),
                                           avg_discount=("Discount","mean"),
                                           unique_customers=("Customer ID","nunique"),
                                           unique_orders=("Order ID","nunique")).reset_index().sort_values("total_profit",ascending=False)
print("\nSegment analysis")
print(segment_analysis)
customer_profit_analysis=df.groupby(["Customer ID","Customer Name"]).agg(total_sales=("Sales","sum"),
                                                                         total_profit=("Profit","sum"),
                                                                         avg_discount=("Discount","mean"),
                                                                         unique_orders=("Order ID","nunique")).reset_index().sort_values("total_profit")
print("\nbottom 10 customers by profit")
print(customer_profit_analysis.head(10))
monthly_analysis=df.groupby("Year-Month").agg(total_sales=("Sales","sum"),
                                               total_profit=("Profit","sum"),
                                               unique_orders=("Order ID","nunique")).reset_index()
print("\n Monthly analysis")
print(monthly_analysis.head(12))
print(monthly_analysis.columns)
plt.figure(figsize=(10,5))
plt.plot(monthly_analysis["Year-Month"].astype(str),monthly_analysis["total_profit"])
plt.title("Monthly profit analysis")
plt.xlabel("Year-Month")
plt.ylabel("Total profit")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("charts/monthly_profit_analysis.png")
plt.show()
customer_analysis=df.groupby("Customer ID").agg(total_sales=("Sales","sum"),
                                                total_profit=("Profit","sum"))
yearly_analysis=df.groupby("Order year").agg(total_sales=("Sales","sum"),
                             total_profit=("Profit","sum"),
                             unique_orders=("Order ID","nunique"),
                             unique_customers=("Customer ID","nunique")).reset_index()
yearly_analysis["Profit_margin_pct"]=(yearly_analysis["total_profit"]/yearly_analysis["total_sales"])*100
print("\nyearly analysis")
print(yearly_analysis)
plt.figure(figsize=(8,5))
plt.bar(yearly_analysis["Order year"],yearly_analysis["total_sales"])
plt.title("Yearly sales")
plt.xlabel("Year")
plt.ylabel("Total sales")
plt.tight_layout()
plt.savefig("charts/yearly_sales_analysis.png")
plt.show()
plt.figure(figsize=(8,5))
plt.bar(yearly_analysis["Order year"],yearly_analysis["total_profit"])
plt.title("Yearly profit")
plt.xlabel("Year")
plt.ylabel("Total profit")
plt.tight_layout()
plt.savefig("charts/yearly_profit_analysis.png")
plt.show()
plt.figure(figsize=(8,5))
plt.plot(yearly_analysis["Order year"],yearly_analysis["Profit_margin_pct"],marker="o")
plt.xlabel("Year")
plt.ylabel("Profit Margin %")
plt.tight_layout()
plt.savefig("charts/yearly_profit_margin.png")
plt.show()
loss_making_products=product_loss_analysis[product_loss_analysis["total_profit"]<0]
print("\n LOSS MAKING PRODUCTS")
print(loss_making_products[["State","Sub-Category","Product Name","total_sales","total_profit","avg_discount"]].head(20))
high_sales_loss_products=loss_making_products.sort_values(by="total_sales",ascending=False).head(10)
print("\n High-sales but loss making products")
print(high_sales_loss_products[["State","Sub-Category","Product Name","total_sales","total_profit","avg_discount"]])
total_sales=df["Sales"].sum()
total_profit=df["Profit"].sum()
total_orders=df["Order ID"].nunique()
total_customers=df["Customer ID"].nunique()
overall_profit_margin=(total_profit/total_sales)*100
print("\n" + "=" * 50)
print("Executive business summary below")
print("="*50)
print(f"Total sales: ${total_sales:,.2f}")
print(f"Total Profit:${total_profit:,.2f}")
print(f"Total orders:{total_orders:,}")
print(f"Total customers:{total_customers:,}")
print(f"Overall Profit Margin:{overall_profit_margin:,.2f}")
best_category=category_analysis.sort_values("total_profit",ascending=False).iloc[0]
worst_category=category_analysis.sort_values("total_profit",ascending=True).iloc[0]
best_state=state_analysis.sort_values("total_profit",ascending=False).iloc[0]
worst_state=state_analysis.sort_values("total_profit").iloc[0]
worst_product=product_loss_analysis.sort_values("total_profit").iloc[0]
print("\n worst loss making product")
print("State:",worst_product["State"])
print("Sub-Category:",worst_product["Sub-Category"])
print("Product:",worst_product["Product Name"])
print("Sales:",round(worst_product["total_sales"],2))
print("Profit:",round(worst_product["total_profit"],2))
print("Average Discount:",round(worst_product["avg_discount"],2))
print("Best category:",best_category["Category"],"| Profit:",round(best_category["total_profit"],2))
print("Worst Category:",worst_category["Category"],"| Profit:",round(worst_category["total_profit"],2))
print("Best state:",best_state["State"],"| Profit:",round(best_state["total_profit"],2))
print("Worst state:",worst_state["State"],"| Profit:",round(worst_state["total_profit"],2))
category_analysis.to_csv("outputs/category_summary.csv",index=False)
state_analysis.to_csv("outputs/geography_summary.csv",index=False)
product_loss_analysis.to_csv("outputs/product_loss_summary.csv",index=False)
discount_band_analysis.to_csv("outputs/discount_summary.csv",index=False)
monthly_analysis.to_csv("outputs/discount_summary.csv",index=False)
yearly_analysis.to_csv("outputs/yearly_summary.csv",index=False)
business_kpi_summary=pd.DataFrame({"Metric":["Total Sales","Total Profit","Profit Margin %","Unique Orders","Unique Customers"],
                                   "Value":[total_sales,total_profit,overall_profit_margin,total_orders,total_customers]})
business_kpi_summary.to_csv("outputs/business_kpi_summary.csv",index=False)
print(business_kpi_summary)