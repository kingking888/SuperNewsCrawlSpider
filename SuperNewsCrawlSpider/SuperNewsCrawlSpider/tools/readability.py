# # #coding=utf-8
# #
# # # author: kingwkb
# # # blog : http://yanghao.org/blog/
# # #
# # # this is code demo: http://yanghao.org/tools/readability
# #
# # from __future__ import division
# # import os
# # import sys
# # import urllib
# # import re
# # import math
# # import posixpath
# # from urllib.parse import urlparse
# # from html.parser import HTMLParser
# #
# # import chardet
# # # from BeautifulSoup import BeautifulSoup
# # from bs4 import BeautifulSoup
# #
# # class Readability(object):
# #
# #     regexps = {
# #         'unlikelyCandidates': re.compile("combx|comment|community|disqus|extra|foot|header|menu|"
# #                                          "remark|rss|shoutbox|sidebar|sponsor|ad-break|agegate|"
# #                                          "pagination|pager|popup|tweet|twitter",re.I),
# #         'okMaybeItsACandidate': re.compile("and|article|body|column|main|shadow", re.I),
# #         'positive': re.compile("article|body|content|entry|hentry|main|page|pagination|post|text|"
# #                                "blog|story",re.I),
# #         'negative': re.compile("combx|comment|com|contact|foot|footer|footnote|masthead|media|"
# #                                "meta|outbrain|promo|related|scroll|shoutbox|sidebar|sponsor|"
# #                                "shopping|tags|tool|widget", re.I),
# #         'extraneous': re.compile("print|archive|comment|discuss|e[\-]?mail|share|reply|all|login|"
# #                                  "sign|single",re.I),
# #         'divToPElements': re.compile("<(a|blockquote|dl|div|img|ol|p|pre|table|ul)",re.I),
# #         'replaceBrs': re.compile("(<br[^>]*>[ \n\r\t]*){2,}",re.I),
# #         'replaceFonts': re.compile("<(/?)font[^>]*>",re.I),
# #         'trim': re.compile("^\s+|\s+$",re.I),
# #         'normalize': re.compile("\s{2,}",re.I),
# #         'killBreaks': re.compile("(<br\s*/?>(\s|&nbsp;?)*)+",re.I),
# #         'videos': re.compile("http://(www\.)?(youtube|vimeo)\.com",re.I),
# #         'skipFootnoteLink': re.compile("^\s*(\[?[a-z0-9]{1,2}\]?|^|edit|citation needed)\s*$",re.I),
# #         'nextLink': re.compile("(next|weiter|continue|>([^\|]|$)|»([^\|]|$))",re.I),
# #         'prevLink': re.compile("(prev|earl|old|new|<|«)",re.I)
# #     }
# #
# #     def __init__(self, input, url):
# #         """
# #         url = "http://yanghao.org/blog/"
# #         htmlcode = urllib2.urlopen(url).read().decode('utf-8')
# #
# #         readability = Readability(htmlcode, url)
# #
# #         print readability.title
# #         print readability.content
# #         """
# #         self.candidates = {}
# #
# #         self.input = input
# #         self.url = url
# #         self.input = self.regexps['replaceBrs'].sub("</p><p>",self.input)
# #         self.input = self.regexps['replaceFonts'].sub("<\g<1>span>",self.input)
# #
# #         self.html = BeautifulSoup(self.input,features="lxml")
# #
# # #        print self.html.originalEncoding
# # #        print self.html
# #         self.removeScript()
# #         self.removeStyle()
# #         self.removeLink()
# #
# #         self.title = self.getArticleTitle()
# #         self.content = self.grabArticle()
# #
# #
# #     def removeScript(self):
# #         for elem in self.html.findAll("script"):
# #             elem.extract()
# #
# #     def removeStyle(self):
# #         for elem in self.html.findAll("style"):
# #             elem.extract()
# #
# #     def removeLink(self):
# #         for elem in self.html.findAll("link"):
# #             elem.extract()
# #
# #     def grabArticle(self):
# #
# #         for elem in self.html.findAll(True):
# #
# #             unlikelyMatchString = elem.get('id','') + elem.get('class','')
# #
# #             if self.regexps['unlikelyCandidates'].search(unlikelyMatchString) and \
# #                 not self.regexps['okMaybeItsACandidate'].search(unlikelyMatchString) and \
# #                 elem.name != 'body':
# # #                print elem
# # #                print '--------------------'
# #                 elem.extract()
# #                 continue
# # #                pass
# #
# #             if elem.name == 'div':
# #                 s = elem.renderContents(encoding=None)
# #                 if not self.regexps['divToPElements'].search(s):
# #                     elem.name = 'p'
# #
# #         for node in self.html.findAll('p'):
# #
# #             parentNode = node.parent
# #             grandParentNode = parentNode.parent
# #             innerText = node.text
# #
# # #            print '=================='
# # #            print node
# # #            print '------------------'
# # #            print parentNode
# #
# #             if not parentNode or len(innerText) < 20:
# #                 continue
# #
# #             parentHash = hash(str(parentNode))
# #             grandParentHash = hash(str(grandParentNode))
# #
# #             if parentHash not in self.candidates:
# #                 self.candidates[parentHash] = self.initializeNode(parentNode)
# #
# #             if grandParentNode and grandParentHash not in self.candidates:
# #                 self.candidates[grandParentHash] = self.initializeNode(grandParentNode)
# #
# #             contentScore = 1
# #             contentScore += innerText.count(',')
# #             contentScore += innerText.count(u'，')
# #             contentScore +=  min(math.floor(len(innerText) / 100), 3)
# #
# #             self.candidates[parentHash]['score'] += contentScore
# #
# # #            print '======================='
# # #            print self.candidates[parentHash]['score']
# # #            print self.candidates[parentHash]['node']
# # #            print '-----------------------'
# # #            print node
# #
# #             if grandParentNode:
# #                 self.candidates[grandParentHash]['score'] += contentScore / 2
# #
# #         topCandidate = None
# #
# #         for key in self.candidates:
# # #            print '======================='
# # #            print self.candidates[key]['score']
# # #            print self.candidates[key]['node']
# #
# #             self.candidates[key]['score'] = self.candidates[key]['score'] * \
# #                                             (1 - self.getLinkDensity(self.candidates[key]['node']))
# #
# #             if not topCandidate or self.candidates[key]['score'] > topCandidate['score']:
# #                 topCandidate = self.candidates[key]
# #
# #         content = ''
# #
# #         if topCandidate:
# #             content = topCandidate['node']
# # #            print content
# #             content = self.cleanArticle(content)
# #         return content
# #
# #
# #     def cleanArticle(self, content):
# #
# #         self.cleanStyle(content)
# #         self.clean(content, 'h1')
# #         self.clean(content, 'object')
# #         self.cleanConditionally(content, "form")
# #
# #         if len(content.findAll('h2')) == 1:
# #             self.clean(content, 'h2')
# #
# #         self.clean(content, 'iframe')
# #
# #         self.cleanConditionally(content, "table")
# #         self.cleanConditionally(content, "ul")
# #         self.cleanConditionally(content, "div")
# #
# #         self.fixImagesPath(content)
# #
# #         content = content.renderContents(encoding=None)
# #
# #         content = self.regexps['killBreaks'].sub("<br />", content)
# #
# #         return content
# #
# #     def clean(self,e ,tag):
# #
# #         targetList = e.findAll(tag)
# #         isEmbed = 0
# #         if tag =='object' or tag == 'embed':
# #             isEmbed = 1
# #
# #         for target in targetList:
# #             attributeValues = ""
# #             for attribute in target.attrs:
# #                 attributeValues += target[attribute[0]]
# #
# #             if isEmbed and self.regexps['videos'].search(attributeValues):
# #                 continue
# #
# #             if isEmbed and self.regexps['videos'].search(target.renderContents(encoding=None)):
# #                 continue
# #             target.extract()
# #
# #     def cleanStyle(self, e):
# #
# #         for elem in e.findAll(True):
# #             del elem['class']
# #             del elem['id']
# #             del elem['style']
# #
# #     def cleanConditionally(self, e, tag):
# #         tagsList = e.findAll(tag)
# #
# #         for node in tagsList:
# #             weight = self.getClassWeight(node)
# #             hashNode = hash(str(node))
# #             if hashNode in self.candidates:
# #                 contentScore = self.candidates[hashNode]['score']
# #             else:
# #                 contentScore = 0
# #
# #             if weight + contentScore < 0:
# #                 node.extract()
# #             else:
# #                 p = len(node.findAll("p"))
# #                 img = len(node.findAll("img"))
# #                 li = len(node.findAll("li"))-100
# #                 input = len(node.findAll("input"))
# #                 embedCount = 0
# #                 embeds = node.findAll("embed")
# #                 for embed in embeds:
# #                     if not self.regexps['videos'].search(embed['src']):
# #                         embedCount += 1
# #                 linkDensity = self.getLinkDensity(node)
# #                 contentLength = len(node.text)
# #                 toRemove = False
# #
# #                 if img > p:
# #                     toRemove = True
# #                 elif li > p and tag != "ul" and tag != "ol":
# #                     toRemove = True
# #                 elif input > math.floor(p/3):
# #                     toRemove = True
# #                 elif contentLength < 25 and (img==0 or img>2):
# #                     toRemove = True
# #                 elif weight < 25 and linkDensity > 0.2:
# #                     toRemove = True
# #                 elif weight >= 25 and linkDensity > 0.5:
# #                     toRemove = True
# #                 elif (embedCount == 1 and contentLength < 35) or embedCount > 1:
# #                     toRemove = True
# #
# #                 if toRemove:
# #                     node.extract()
# #
# #
# #     def getArticleTitle(self):
# #         title = ''
# #         try:
# #             title = self.html.find('title').text
# #         except:
# #             pass
# #
# #         return title
# #
# #
# #     def initializeNode(self, node):
# #         contentScore = 0
# #
# #         if node.name == 'div':
# #             contentScore += 5
# #         elif node.name == 'blockquote':
# #             contentScore += 3
# #         elif node.name == 'form':
# #             contentScore -= 3
# #         elif node.name == 'th':
# #             contentScore -= 5
# #
# #         contentScore += self.getClassWeight(node)
# #
# #         return {'score':contentScore, 'node': node}
# #
# #     def getClassWeight(self, node):
# #         weight = 0
# #         if 'class' in node:
# #             if self.regexps['negative'].search(node['class']):
# #                 weight -= 25
# #             if self.regexps['positive'].search(node['class']):
# #                 weight += 25
# #
# #         if 'id' in node:
# #             if self.regexps['negative'].search(node['id']):
# #                 weight -= 25
# #             if self.regexps['positive'].search(node['id']):
# #                 weight += 25
# #
# #         return weight
# #
# #     def getLinkDensity(self, node):
# #         links = node.findAll('a')
# #         textLength = len(node.text)
# #
# #         if textLength == 0:
# #             return 0
# #         linkLength = 0
# #         for link in links:
# #             linkLength += len(link.text)
# #
# #         return linkLength / textLength
# #
# #     def fixImagesPath(self, node):
# #         imgs = node.findAll('img')
# #         for img in imgs:
# #             src = img.get('src',None)
# #             if not src:
# #                 img.extract()
# #                 continue
# #
# #             if 'http://' != src[:7] and 'https://' != src[:8]:
# #                 newSrc = urlparse.urljoin(self.url, src)
# #
# #                 newSrcArr = urlparse.urlparse(newSrc)
# #                 newPath = posixpath.normpath(newSrcArr[2])
# #                 newSrc = urlparse.urlunparse((newSrcArr.scheme, newSrcArr.netloc, newPath,
# #                                               newSrcArr.params, newSrcArr.query, newSrcArr.fragment))
# #                 img['src'] = newSrc
#
#
# from bs4 import BeautifulSoup, NavigableString, Comment
# import re
# import copy
#
#
#
# class Readability(object):
#     div_to_p_elems = ["a", "blockquote", "dl", "div", "img", "ol", "p", "pre", "table", "ul", "select"]
#
#     REGEXES = {
#         'unlikelyCandidatesRe': re.compile(
#             'combx|comment|community|disqus|extra|foot|header|menu|remark|rss|shoutbox|sidebar|sponsor|ad-break|agegate|pagination|pager|popup|tweet|twitter',
#             re.I),
#         'okMaybeItsACandidateRe': re.compile('and|article|body|column|main|shadow', re.I),
#         'positiveRe': re.compile('article|body|content|entry|hentry|main|page|pagination|post|text|blog|story', re.I),
#         'negativeRe': re.compile(
#             'combx|comment|com-|contact|foot|footer|footnote|masthead|media|meta|outbrain|promo|related|scroll|shoutbox|sidebar|sponsor|shopping|tags|tool|widget',
#             re.I),
#         'divToPElementsRe': re.compile('<(a|blockquote|dl|div|img|ol|p|pre|table|ul)', re.I),
#         # 'replaceBrsRe': re.compile('(<br[^>]*>[ \n\r\t]*){2,}',re.I),
#         # 'replaceFontsRe': re.compile('<(\/?)font[^>]*>',re.I),
#         # 'trimRe': re.compile('^\s+|\s+$/'),
#         # 'normalizeRe': re.compile('\s{2,}/'),
#         # 'killBreaksRe': re.compile('(<br\s*\/?>(\s|&nbsp;?)*){1,}/'),
#         'videoRe': re.compile('https?:\/\/(www\.)?(youtube|vimeo)\.com', re.I),
#         'attributeRe': re.compile('blog|post|article', re.I),
#         # skipFootnoteLink:      /^\s*(\[?[a-z0-9]{1,2}\]?|^|edit|citation needed)\s*$/i,
#     }
#
#     def __init__(self, html, preserveUnlikelyCandidates=False):
#         self.html = html
#         self.preserveUnlikelyCandidates = preserveUnlikelyCandidates
#         self.title = ''
#         self.article = ''
#         self.soup = None
#
#     def minify(self, html):
#         # minified = re.sub('\n+','\n',re.sub('\n+','\n',re.sub(' +',' ',re.sub('\t','',html))))
#         minified = re.sub('\n+', '\n', re.sub('<!--.*?-->', '', re.sub('<script.*?</script>', '',
#                                                                        re.sub('<script.*?[^>]*</script>', '',
#                                                                               re.sub('<!--[^>]*-->', '',
#                                                                                      re.sub(' <', '<', re.sub('> ', '>',
#                                                                                                               re.sub(
#                                                                                                                   '> <',
#                                                                                                                   '><',
#                                                                                                                   re.sub(
#                                                                                                                       ' +',
#                                                                                                                       ' ',
#                                                                                                                       re.sub(
#                                                                                                                           '\t',
#                                                                                                                           '',
#                                                                                                                           html)))))))).strip()))
#         return minified
#
#     def RepresentsInt(self, s):
#         try:
#             int(s)
#             return True
#         except ValueError:
#             return False
#
#     def getClassWeight(self, node):
#         weight = 0
#
#         if node.has_attr('class'):
#             classNames = ' '.join(node['class'])
#             if self.REGEXES['negativeRe'].search(classNames):
#                 weight -= 25
#             if self.REGEXES['positiveRe'].search(classNames):
#                 weight += 25
#         if node.has_attr('id') and not self.RepresentsInt(node['id']):
#             if self.REGEXES['negativeRe'].search(node['id']):
#                 weight -= 25
#             if self.REGEXES['positiveRe'].search(node['id']):
#                 weight += 25
#         return weight
#
#     def initializeNode(self, node):
#         node['readability-score'] = 0
#
#         score_weight = {
#             'article': 10,
#             'section': 8,
#             'div': 5,
#             'pre': 3,
#             'td': 3,
#             'blockquote': 3,
#             'address': -3,
#             'ol': -3,
#             'ul': -3,
#             'dl': -3,
#             'dd': -3,
#             'dt': -3,
#             'li': -3,
#             'form': -3,
#             'h1': -5,
#             'h2': -5,
#             'h3': -5,
#             'h4': -5,
#             'h5': -5,
#             'h6': -5,
#             'th': -5,
#         }
#         node['readability-score'] += score_weight.get(node.name, 0)
#
#         if node.has_attr('itemscope'):
#             node['readability-score'] += 5
#             if node.has_attr('itemtype') and self.REGEXES['attributeRe'].search(node['itemtype']):
#                 node['readability-score'] += 30
#         node['readability-score'] += self.getClassWeight(node)
#
#     def getInnerText(self, elem):
#         textContent = str(elem.text).strip()
#         textContent = textContent.replace('\s{2,}/g', ' ')
#         return textContent.strip()
#
#     def getLinkDensity(self, elem):
#         textLength = len(self.getInnerText(elem))
#         if textLength == 0:
#             return 0
#         linkLength = 0
#         for atag in elem.findAll("a"):
#             try:
#                 if atag['href'][0] == "#":
#                     continue
#                 linkLength += len(self.getInnerText(atag))
#             except KeyError:
#                 continue
#         return linkLength / textLength
#
#     def getArticleMetadata(self):
#         metadata = {}
#         values = {}
#         # property is a space-separated list of values
#         propertyPattern = "\s*(dc|dcterm|og|twitter)\s*\:\s*(author|creator|description|title|site_name|type)\s*"
#
#         # name is a single value
#         namePattern = "^\s*(?:(dc|dcterm|og|twitter|weibo:(article|webpage))\s*[\.:]\s*)?(author|creator|description|title|site_name|type)\s*$"
#
#         for meta in self.soup.find_all('meta'):
#             elementName = meta.get("name", "")
#             elementProperty = meta.get("property", "")
#             content = meta.get("content", "")
#             matches = None
#             name = None
#             matches = re.findall(propertyPattern, elementProperty)
#
#             if elementProperty:
#                 if matches:
#                     for match in matches:
#                         if isinstance(match, tuple):
#                             name = ":".join(list(match)).replace("\s", '')
#                         else:
#                             name = match.lower().replace('\s', '')
#                         values[name] = content.strip()
#             if not matches and elementName and re.search(namePattern, elementName):
#                 name = elementName
#                 if content:
#                     name = name.lower().replace('\s', '').replace('.', ':')
#                     values[name] = content.strip()
#
#         metadata = {
#             # get title
#             "title": values.get("dc:title") or
#                      values.get("dcterm:title") or
#                      values.get("og:title") or
#                      values.get("weibo:article:title") or
#                      values.get("weibo:webpage:title") or
#                      values.get("title") or
#                      values.get("twitter:title"),
#             # get author
#             "byline": values.get("dc:creator") or
#                       values.get("dcterm:creator") or
#                       values.get("author"),
#             # get description
#             "excerpt": values.get("dc:description") or
#                        values.get("dcterm:description") or
#                        values.get("og:description") or
#                        values.get("weibo:article:description") or
#                        values.get("weibo:webpage:description") or
#                        values.get("description") or
#                        values.get("twitter:description"),
#             # get type
#             "type": values.get("og:type", "default"),
#             # get site name
#             "siteName": values.get("og:site_name")
#         }
#
#         return metadata
#
#     # def get_own_textContent(element):
#     # 	textContent=''
#     # 	if not isinstance(element, NavigableString):
#     # 		if hasattr(element, 'children'):
#     # 			for child in element.children:
#     # 				if isinstance(child, NavigableString):
#     # 					textContent+=str(child);
#     # 	if textContent == '':
#     # 		return None
#     # 	else:
#     # 		return re.sub('\n+','\n', textContent.strip())
#
#     @staticmethod
#     def removeScripts(soup):
#         [s.extract() for s in soup('script')]
#         return soup
#
#     @staticmethod
#     def removeComments(soup):
#         for element in soup.find_all():
#             if isinstance(element, Comment):
#                 element.extract()
#         return soup
#
#     @staticmethod
#     def removeElements(soup):
#         for element in soup:
#             element.extract()
#         return soup
#
#     def grabArticle(self):
#         for node in self.soup.findAll():
#             continueFlag = False
#             if not self.preserveUnlikelyCandidates:
#                 classNames = ''
#                 if node.has_attr('class'):
#                     classNames = ' '.join(node['class'])
#                 idName = ''
#                 if node.has_attr('id'):
#                     idName = node['id']
#                 unlikelyMatchString = classNames + idName
#                 if self.REGEXES['unlikelyCandidatesRe'].search(unlikelyMatchString) and not self.REGEXES[
#                     'okMaybeItsACandidateRe'].search(
#                         unlikelyMatchString) and node.name != 'html' and node.name != 'body':
#                     node.extract()
#                     continueFlag = True
#
#             if not continueFlag and node.name == "div":
#                 if not self.REGEXES['divToPElementsRe'].search(str(node)):
#                     node.name = "p"
#                 else:
#                     for child in node.children:
#                         if isinstance(child, NavigableString) and str(child).strip() != "":
#                             new_p = self.soup.new_tag('p')
#                             new_p.append(str(child))
#                             child.insert_before(new_p)
#                             child.extract()
#
#         candidates = []
#         for paragraph in self.soup.findAll('p'):
#             parentNode = paragraph.parent
#             grandParentNode = parentNode.parent
#             InnerText = self.getInnerText(paragraph)
#
#             if len(InnerText) < 25:
#                 continue
#             if not parentNode.has_attr('readability-score'):
#                 self.initializeNode(parentNode)
#                 candidates.append(parentNode)
#             if not grandParentNode.has_attr('readability-score'):
#                 self.initializeNode(grandParentNode)
#                 candidates.append(grandParentNode)
#
#             contentScore = 0
#
#             # Add a point for the paragraph itself as a base.
#             contentScore += 1
#
#             # For every 100 characters in this paragraph, add another point. Up to 3 points.
#             contentScore += min(len(InnerText) / 100, 3)
#             # Add the score to the parent. The grandparent gets half.
#             parentNode['readability-score'] += contentScore;
#             grandParentNode['readability-score'] += contentScore / 2;
#
#         topCandidate = {}
#         # get top candidate
#         for candidate in candidates:
#             candidate['readability-score'] = candidate['readability-score'] * (1 - self.getLinkDensity(candidate))
#             if not topCandidate or candidate['readability-score'] > topCandidate['readability-score']:
#                 topCandidate = candidate
#
#         '''
#         Now that we have the top candidate, look through its siblings for content that might also be related.
#         Things like preambles, content split by ads that we removed, etc.
#         '''
#
#         if topCandidate:
#             articleContent = self.soup.new_tag('div')
#             articleContent['id'] = 'readability-content'
#
#             siblingsScoreThreshold = max(10, topCandidate['readability-score'] * 0.2);
#
#             siblingNodes = topCandidate.parent.children
#
#             for siblingNode in siblingNodes:
#                 if not isinstance(siblingNode, NavigableString):
#                     append = False
#
#                     if siblingNode == topCandidate:
#                         append = True
#
#                     if siblingNode.has_attr('readability-score') and siblingNode[
#                         'readability-score'] >= siblingsScoreThreshold:
#                         append = True
#
#                     if siblingNode.name == "p":
#                         linkDensity = self.getLinkDensity(siblingNode)
#                         nodeContent = self.getInnerText(siblingNode)
#                         nodeLength = len(nodeContent)
#
#                         if nodeLength > 80 and linkDensity == 0 and re.search('/\.( |$)/', nodeContent):
#                             append = True
#
#                     if append:
#                         articleContent.append(copy.copy(siblingNode))
#             return articleContent
#         else:
#             return topCandidate
#
#     def parse(self):
#         ### MINIFY HTML
#         html = self.minify(self.html)
#
#         self.soup = BeautifulSoup(html, 'html5lib')
#         self.soup = self.removeScripts(self.soup)
#         self.soup = self.removeComments(self.soup)
#
#         self.removeElements(self.soup.find_all('style'))
#
#         metadata = self.getArticleMetadata()
#         article = self.grabArticle()
#
#         return {
#             **metadata,
#             # "textContent": self.minify(article.get("text", "")),
#             "textContent": self.minify(article.text),
#             "content": str(article)
#         }