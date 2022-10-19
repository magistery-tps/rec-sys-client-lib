import seaborn as sns

sns.set_style("white")
sns.despine()

s_size   = lambda: sns.set(rc={'figure.figsize':(5,5)})

m_size   = lambda: sns.set(rc={'figure.figsize':(10, 6)})

l_flat_size   = lambda: sns.set(rc={'figure.figsize':(15, 4)})

l_size   = lambda: sns.set(rc={'figure.figsize':(15, 8)})

xl_flat_size  = lambda: sns.set(rc={'figure.figsize':(20, 5)})
xl_size  = lambda: sns.set(rc={'figure.figsize':(20, 15)})

xxl_flat_size  = lambda: sns.set(rc={'figure.figsize':(30, 10)})
xxl_size  = lambda: sns.set(rc={'figure.figsize':(30, 15)})


m_size()