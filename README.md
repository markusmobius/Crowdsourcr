
#### To give user-mode access to port 80:

 iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

### Exclusions

Each HIT may specify a set of exclusions, a comma separated list of other HIT IDs such that if a worker has completed any of the HITs listed as exclusions she may not complete the HIT that listed those exlclusions. Perhaps an example would be most informative. Consider the following HITs:

```xml
  <hits>
    <hit>
      <hitid>1</hitid>
      <exclusions>2</exclusions>
      <tasks>
	1
	2
      </tasks>
    </hit>
    <hit>
      <hitid>2</hitid>
      <tasks>
	1
      </tasks>
    </hit> 
  </hits>
```

In this case, a worker who first completes HIT 2 may not then complete HIT 1, since HIT 1 excludes HIT 2. However, since HIT 2 lists no exclusions, a worker who first completes HIT 1 would then be permitted to complete HIT 2. There is no enforcement that exclusions be symmetric.


### Scale Questions

After the scale question type was dropped from a previous release, scale questions must now be added as categorical types. All questions may have an options tag, and the nested layout tag specifies whether the radio buttons are rendered horizontally or vertically (the latter being the default). Several other options are available, as in the following example:

```xml
<options>
  <layout>horizontal</layout>
  <lowLabel>Conservative</lowLabel>
  <highLabel>Liberal</highLabel>
  <outsideCategories>N/A</outsideCategories>
  <outsideCategories>Unsure</outsideCategories>
</options>
```

This will yield the following layout:

![new project](https://github.com/sgrondahl/news_crowdsourcer/raw/master/markdown/ScaleQuestion.PNG)


### Nested Categorical Questions

See src/tests/test_xml_cat_expand_1.xml for example usage. To control nesting, encode nests in text tags, i.e. 

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
