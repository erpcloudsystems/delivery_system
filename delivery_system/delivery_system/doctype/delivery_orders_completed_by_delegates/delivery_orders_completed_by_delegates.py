# -*- coding: utf-8 -*-
# Copyright (c) 2020, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date
from frappe import msgprint, throw, _
from frappe.utils import flt
from delivery_system import set_order_amounts, set_address_and_contact

class DeliveryOrdersCompletedByDelegates(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order)
		set_address_and_contact(self,self.sales_order)