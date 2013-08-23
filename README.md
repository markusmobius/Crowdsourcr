

#### To give user-mode access to port 80:

 iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080


### Nested Categorical Questions

See src/tests/test_xml_cat_expand_1.xml for example usage. To control nesting, encode nests in <text>, i.e. 

```xml
<text> Hard News | Science and Tech | Computers </text>.
```

The <value> will be sent along if the rightmost category is selected. It is possible to have asymmetric trees, so in addition to the above you could add 

```xml
<text> Hard News | Politics </text>.
```

Then if the user selects Hard News > Politics, no more expansion will happen and the question will be complete. Technically it is also possible to have optional specificity, i.e. add a category with 

```xml
<text> Hard News | Politics | National </text>
```

This would allow selection of either HN > Politics or HN > Politics > National, and both would be acceptable. In this case the final expansion will occur to show "National", but technically the user could continue without selecting it and not receive an error.