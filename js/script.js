const drawer = () => {
  const links = document.querySelectorAll('.navigation__link')
  const openBtn = document.querySelector('#open-btn')
  const closeBtn = document.querySelector('#close-btn')
  const body = document.querySelector('body')
  const navigation = document.querySelector('#navigation')

  const open = () => {
    body.classList.add('no-scroll')
    navigation.classList.add('navigation_active')
  }
  const close = () => {
    body.classList.remove('no-scroll')
    navigation.classList.remove('navigation_active')
  }

  openBtn.addEventListener('click', open)
  closeBtn.addEventListener('click', close)
  links.forEach(link => link.addEventListener('click', close))
}

const sticky = () => {
  const header = document.querySelector('#header')

  const onScroll = () => {
    if (document.documentElement.scrollTop > 90) {
      header.classList.add('header-wrapper_sticky')
    } else {
      header.classList.remove('header-wrapper_sticky')
    }
  }

  window.addEventListener('scroll', onScroll)
}

const highlight = () => {
  const links = document.querySelectorAll('.navigation__link')
  const sections = document.querySelectorAll('#home,#about,#skills,#portfolio,#contacts')
  const weights = Array(sections.length).fill(0)

  const onScroll = () => {
    const top = document.documentElement.scrollTop
    const bottom = top + window.innerHeight

    sections.forEach((section, index) => {
      const { offsetTop, offsetHeight } = section
      const offsetBottom = offsetTop + offsetHeight
      const isIntersecting = (bottom > offsetTop) && (top < (offsetTop + offsetHeight))

      if (!isIntersecting) {
        weights[index] = 0
        return
      }
      if (offsetTop < bottom && offsetTop > top) {
        weights[index] = bottom - offsetTop
      }
      if (offsetBottom > top && offsetBottom < bottom) {
        weights[index] = offsetBottom - top
      }
    })

    const maxWeight = Math.max(...weights)
    const activeIndex = weights.indexOf(maxWeight)

    links.forEach(link => link.classList.remove('navigation__link_active'))
    links[activeIndex].classList.add('navigation__link_active')
  }

  onScroll()
  window.addEventListener('scroll', onScroll)
}

document.addEventListener('DOMContentLoaded', () => {
  drawer()
  sticky()
  highlight()
})
