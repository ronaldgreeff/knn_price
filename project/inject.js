function util__strip(str) {
  return str.replace(/^\s+|\s+$/g, '');
}

function util__path(element) {
  let selector = "";
  while (element.parentElement) {
    const siblings = Array.from(element.parentElement.children).filter(
      e => e.tagName === element.tagName
    );
    selector =
      (siblings.indexOf(element)
        ? `${element.tagName}:nth-of-type(${siblings.indexOf(element) + 1})`
        : `${element.tagName}`) + `${selector ? " > " : ""}${selector}`;
    element = element.parentElement;
  }
  return `html > ${selector.toLowerCase()}`;
};

function util__computed(element) {
  var computed, data, defaults, key, _i, _len;
  defaults = document.defaultView.getComputedStyle(document.body);
  computed = document.defaultView.getComputedStyle(element);
  data = {};
  for (_i = 0, _len = computed.length; _i < _len; _i++) {
    key = computed[_i];
    if (key === 'width' || key === 'height' || key === 'top' || key === 'left' || key === 'right' || key === 'bottom') {
      continue;
    }
    if (key.charAt(0) === '-') {
      continue;
    }
    if (computed[key] === defaults[key]) {
      continue;
    }
    data[key] = computed[key];
  }
  return data;
};

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
    else if (bound.top > window.innerHeight || (bound.top + bound.height) > window.innerHeight ) {
        continue;
    }
    while (node) {
      computed = document.defaultView.getComputedStyle(node);
      if (parseInt(computed.width) * parseInt(computed.height) > 0) {
        break;
      }
      node = node.parentElement;
    }
    if (!node) {
      continue;
    }
    if (node.__spider) {
      node.__spider.text.push(util__strip(text.nodeValue));
      continue
    }
    node.__spider = {
      text: [util__strip(text.nodeValue)],
      html: node.innerHTML,
      bound: util__bound(node),
      computed: util__computed(node),
      path: util__path(node),
    };
    texts.push(node.__spider);
    // node.style.border = '1px solid red';
  }
  return texts;
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
  var links = extractor__extract_links();

  data['texts'] = texts;
  data['links'] = links;

  data['env'] = {
    window_height: window.innerHeight,
    window_width: window.innerWidth,
    defaults: function(){
      var dflt = document.defaultView.getComputedStyle(document.body);
      d = {};
      for (_i = 0, _len = dflt.length; _i < _len; _i++) {
          key = dflt[_i];
          if (key === 'width' || key === 'height' || key === 'top' || key === 'left' || key === 'right' || key === 'bottom') {
            continue;
          }
          if (key.charAt(0) === '-') {
            continue;
          }
          d[key] = dflt[key];
      }
      return d
    }()

  };
  return data;
};

var data = extract();

return data;
