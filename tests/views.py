import unittest

from flask import request
from flask_wtf import FlaskForm
from mock import Mock, patch

from app.views import BaseView


class BaseViewTests(unittest.TestCase):

    def setUp(self):
        self.view = BaseView()

    def tearDown(self):
        # reset title
        BaseView.Meta.title = None
        # reset form
        BaseView.Meta.form = None
        # reset template
        BaseView.Meta.template = None

    def test_BaseView_title_property_must_return_None_if_not_specified_in_Meta(self):
        self.assertIsNone(self.view.Meta.title)
        self.assertIsNone(self.view.__title__)
        self.assertIsNone(self.view.title)

    def test_BaseView_title_property_must_setted_title(self):
        expected_title = 'title'
        self.view.title = expected_title
        # title not setted
        self.assertIsNotNone(self.view.__title__)
        # title is set
        self.assertEqual(self.view.title, expected_title)

    def test_BaseView_title_property_must_getted_from_Meta_if_specified(self):
        expected_title = 'title'
        # title not setted
        self.assertIsNone(self.view.title)
        # manually set title
        self.view.Meta.title = expected_title
        self.assertEqual(self.view.title, expected_title)

    def test_BaseView_form_attribute_must_be_None_if_not_specified_in_Meta(self):
        # View Form not specified in class Meta
        self.assertIsNone(self.view.Meta.form)

        self.assertIsNone(self.view.form)

    @staticmethod
    def test_BaseView_form_attribute_must_be_instance_of_FlaskForm():
        mocked_form = Mock(FlaskForm)
        BaseView.Meta.form = mocked_form

        # init new instance BaseView with form specified
        BaseView()
        # in init method BaseView must init form class and save form instance
        mocked_form.assert_called()

    def test_BaseView_template_property_must_return_attribute_from_Meta(self):
        """
        template not specified
        """
        self.assertIsNone(self.view.Meta.template)
        self.assertIsNone(self.view.template)

    def test_BaseView_template_property_must_return_attribute_from_Meta(self):
        """
        template specified
        """
        expected_template = 'some_template.html'
        BaseView.Meta.template = expected_template
        # view with template
        new_view = BaseView()

        self.assertEqual(new_view.template, expected_template)

    @patch('app.views.url_for')
    def test_BaseView_default_page_property_must_return_url_for_home(self, mocked_url):
        """
        When default page is not specified property must return '/'
        """
        expected_route = 'home'

        self.view.default_page
        mocked_url.assert_called_with(expected_route)

    @staticmethod
    @patch('app.views.url_for')
    def test_BaseView_default_page_property_must_return_url_for_home_if_Meta_default_page_not_specified(mocked_url):
        """
        When default page is not specified property must return '/'
        """
        BaseView.Meta.default_page = None

        expected_route = '/'

        new_view = BaseView()
        new_view.default_page
        mocked_url.assert_called_with(expected_route)

    @patch('flask_wtf.FlaskForm.validate_on_submit')
    def test_BaseView_is_post_method_must_return_value_from_FlaskForm_validate_on_submit_call(self, mocked_submit):
        # set form to view
        self.view.form = FlaskForm
        # call Form.validate_on_submit()
        self.view.is_post()
        mocked_submit.assert_called_once()

    @patch('flask_wtf.FlaskForm.validate_on_submit', return_value=True)
    def test_BaseView_is_post_method_must_return_True(self, _):
        # set form to view
        self.view.form = FlaskForm
        # call Form.validate_on_submit()
        self.assertTrue(self.view.is_post())

    @patch('flask_wtf.FlaskForm.validate_on_submit', return_value=False)
    def test_BaseView_is_post_method_must_return_True(self, _):
        # set form to view
        self.view.form = FlaskForm
        # call Form.validate_on_submit()
        self.assertFalse(self.view.is_post())

    @patch('app.views.request', spec=request)
    def test_BaseView_is_get_method_must_return_True_for_GET(self, mocked_request):
        mocked_request.method = 'GET'

        self.assertTrue(self.view.is_get())

    @patch('app.views.request', spec=request)
    def test_BaseView_is_get_method_must_return_True_for_GET(self, mocked_request):
        for method in ('POST', 'PUT', 'DELETE', 'OPTIONS'):  # etc
            # check all other methods too
            with self.subTest(method=method):
                mocked_request.method = method
                self.assertFalse(self.view.is_get())

        mocked_request.method = 'POST'
        self.assertFalse(self.view.is_get())

    @staticmethod
    @patch('app.views.render_template')
    def test_BaseView_render_own_template_method_must_call_render_template_function_with_param_at_default(mock_render):
        """
        Default param is:
            -   template
            -   title
            -   form
        """
        BaseView.Meta.form = Mock(return_value='form')
        BaseView.Meta.title = 'title'
        BaseView.Meta.template = 'template'
        expected_kwargs = {
            '__title__': 'title',
            'form': 'form'
        }
        new_view = BaseView()
        new_view._render_own_template()
        mock_render.assert_called_once_with('template', **expected_kwargs)

    @staticmethod
    @patch('app.views.render_template')
    def test_BaseView_render_own_template_method_must_call_render_template_function_with_params(mock_render):
        """
        Default param is:
            -   template
            -   title
            -   form
        """
        BaseView.Meta.form = Mock(return_value='form')
        BaseView.Meta.title = 'title'
        BaseView.Meta.template = 'template'
        expected_kwargs = {
            '__title__': 'title',
            'form': 'form',
        }
        additional_kwargs_to_render = {
            'param1': 'param1',
            'param2': 'param2'
        }

        new_view = BaseView()
        new_view._render_own_template(**additional_kwargs_to_render)
        mock_render.assert_called_once_with('template', **expected_kwargs, **additional_kwargs_to_render)
