from django.shortcuts import render


def home(request):
    latest_pieces = [
        {
            'name': 'Amber Stillness',
            'medium': 'Oil',
            'price': '$100',
            'image': 'marketplace/images/piece-amber.svg',
        },
        {
            'name': 'Blue Hour Study',
            'medium': 'Watercolor',
            'price': '$100',
            'image': 'marketplace/images/piece-blue.svg',
        },
        {
            'name': 'Quiet Geometry',
            'medium': 'Acrylic',
            'price': '$100',
            'image': 'marketplace/images/piece-geometry.svg',
        },
    ]

    return render(request, 'marketplace/index.html', {'latest_pieces': latest_pieces})
