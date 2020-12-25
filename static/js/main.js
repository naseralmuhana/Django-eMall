// const reviewsBox = document.getElementById('reviews-box')
// const spinnerBox = document.getElementById('spinner-box')
// const loadBtn = document.getElementById('load-btn')
// const loadBox = document.getElementById('loading-box')
// const star_rating = document.getElementsByClassName('star-rating')
// let visible = 3

// const handleGetData = () => {
//     $.ajax({
//         type: 'GET',
//         url: `/reviews-json/${visible}`,
//         success: function (response) {
//             maxSize = response.max
//             const data = response.data
//             spinnerBox.classList.remove('not-visible')
//             setTimeout(() => {
//                 spinnerBox.classList.add('not-visible')
//                 data.map(comment => {
//                     console.log(comment)
//                     var comment_rating = comment.rating
//                     empty_star = 5 - comment_rating;
//                     star_rating.innerHTML = ``;
//                     for (var i = 1; i <= comment_rating; i++) {
//                         star_rating.innerHTML += `<i class="sr-star czi-star-filled active"></i>`
//                     }
//                     for (var i = 1; i <= empty_star; i++) {
//                         star_rating.innerHTML += `<i class="sr-star czi-star-filled"></i>`
//                     }
//                     reviewsBox.innerHTML +=
//                         `<div class="product-review pb-4 mb-4 border-bottom">
//                             <div class="d-flex mb-3">
//                                 <div class="media media-ie-fix align-items-center mr-4 pr-2"><img class="rounded-circle"
//                                         width="50" src="{% static 'img/shop/reviews/01.jpg' %}" alt="Rafael Marquez" />
//                                     <div class="media-body pl-3">
//                                         <h6 class="font-size-sm mb-0">
//                                         ${comment.user_id}
//                                         </h6>
//                                         <span class="font-size-ms text-muted">
//                                         ${comment.create_at}
//                                         </span>
//                                     </div>
//                                 </div>
//                                 <div>
//                                     <div class="star-rating">
//                                     ${star_rating.innerHTML}
//                                     </div>
//                                 </div>
//                             </div>
//                             <p class="font-size-md mb-2">
//                             ${comment.review}
//                             </p>
//                         </div>`
//                     star_rating.innerHTML = ``
//                 })
//                 if (maxSize) {
//                     console.log('done')
//                     loadBox.innerHTML = "<h4>No more posts to load</h4>"
//                 }
//             }, 500)
//         },
//         error: function (error) {
//             console.log(error)
//         }
//     })
// }

// handleGetData()

// loadBtn.addEventListener('click', () => {
//     visible += 3
//     handleGetData()
// })



// class ReviewListView(View):
//     def get(self, *args, **kwargs):
//         print(kwargs.get('num_reviews'))
//         upper = kwargs.get('num_reviews')
//         lower = upper - 3
//         reviews = list(core_models.Comment.objects.values()[lower:upper])
//         reviews_size = len(core_models.Comment.objects.all())
//         max_size = True if upper >= reviews_size else False
//         return JsonResponse({'data': reviews, 'max': max_size, 'reviews_size': reviews_size}, safe=False)


