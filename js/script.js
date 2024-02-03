const drawer = () => {
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
}

document.addEventListener('DOMContentLoaded', () => {
  drawer()
})
