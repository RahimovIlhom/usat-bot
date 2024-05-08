from django.shortcuts import render, redirect


def redirect_admin(request):
    return redirect('/admin')
