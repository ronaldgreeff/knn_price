function util__bound(element) {
    var bound, rect, scrollLeft, scrollTop;
    scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    scrollLeft = document.documentElement.scrollLeft || document.body.scrollLeft;
    rect = element.getBoundingClientRect();
    bound = {
      width: rect.width,
      height: rect.height,
      left: rect.left + scrollLeft,
      top: rect.top + scrollTop
    };
    return bound;
  };

function extractor__extract_texts() {
  var bound, computed, node, text, texts, walker;
  texts = [];
  walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  while (text = walker.nextNode()) {
    if (!(text.nodeValue.trim().length > 0)) {
      continue;
    }
    node = text.parentElement;
    bound = util__bound(node);
    if (!(bound.width * bound.height > 0)) {
      continue;
    }
    else if (bound.top > window.innerHeight) {
        continue;
    }
    // while (node) {
    //   computed = document.defaultView.getComputedStyle(node);
    //   if (parseInt(computed.width) * parseInt(computed.height) > 0) {
    //     break;
    //   }
    //   node = node.parentElement;
    // }
    if (!node) {
      continue;
    }
    if (node.__spider) {
      node.__spider.text.push(text.nodeValue);
      continue
    }
    node.__spider = {
      text: [text.nodeValue],
      html: node.innerHTML,
      bound: util__bound(node),
    };
    texts.push(node.__spider);
    node.style.border = '1px solid red';
  }
  return texts;
};

function extractor__extract_images() {
  var bound, images, node, _i, _len, _ref;
  images = [];
  _ref = document.querySelectorAll('img[src]');
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    node = _ref[_i];
    bound = util__bound(node);
    if (!(bound.width * bound.height > 0)) {
      continue;
    }
    images.push({
      src: node.src,
      bound: bound,
    });
    node.style.border = '1px solid red';
  }
  return images;
};

function extractor__extract_links() {
  var link, _i, _len, _ref, _results;
  _ref = document.querySelectorAll('a[href]');
  _results = [];
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    link = _ref[_i];
    _results.push(link.href);
  }
  return _results
};

function extract() {
  var data = {};

  var texts = extractor__extract_texts();
  var images = extractor__extract_images();
  var links = extractor__extract_links();

  data['texts'] = texts;
  data['images'] = images;
  data['links'] = links;

  return data;
};

var data = extract();