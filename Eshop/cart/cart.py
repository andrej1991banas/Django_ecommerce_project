

class Cart():
    def __init__(self, request):
        self.session = request.session

        #get the current session key if exists
        cart=self.session.get('session_key')

        #if user is new, no session key and create one
        if 'session_key' not in request.session:
            cart=self.session['session_key'] = {}

        #make sur cart is available on all paes of site
        self.cart=cart


