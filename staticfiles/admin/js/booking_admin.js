(function($) {
    $(document).ready(function() {
        var $statusField = $('#id_status');
        var $rejectionReasonField = $('#id_rejection_reason');
        var $rejectionReasonRow = $rejectionReasonField.closest('.form-row');

        function toggleRejectionReason() {
            if ($statusField.val() === 'rejected') {
                $rejectionReasonRow.show();
            } else {
                $rejectionReasonRow.hide();
            }
        }

        $statusField.change(toggleRejectionReason);
        toggleRejectionReason();

        $('input[name="_save"]').click(function(e) {
            if ($statusField.val() === 'rejected' && !$rejectionReasonField.val().trim()) {
                e.preventDefault();
                alert('Please provide a reason for rejection.');
            }
        });
    });
})(django.jQuery);